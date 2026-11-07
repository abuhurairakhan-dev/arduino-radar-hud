import re
import time
import queue
import threading
from typing import Optional, Tuple, List
import serial
import serial.tools.list_ports

class SerialManager:
    """Manages serial connection to Arduino with auto-detection and background reading."""
    def __init__(self, baud_rate: int = 115200):
        self.baud_rate = baud_rate
        self.current_port: Optional[str] = None
        self.serial_inst: Optional[serial.Serial] = None
        self.is_connected = False
        self.connection_status = "DISCONNECTED"
        self.rx_queue: queue.Queue = queue.Queue(maxsize=1000)
        self.stop_event = threading.Event()
        self.thread: Optional[threading.Thread] = None

        # Regex patterns for parsing Arduino output formats
        self.re_keyval = re.compile(r"angle(?:_deg)?\s*:\s*(\d+).*?distance(?:_cm)?\s*:\s*([\d\.]+|out_of_range)", re.IGNORECASE)
        self.re_csv = re.compile(r"^\s*(\d+)\s*,\s*([\d\.]+|out_of_range|-1)", re.IGNORECASE)

    def list_available_ports(self) -> List[Tuple[str, str]]:
        """Returns list of (port_name, description)."""
        ports = serial.tools.list_ports.comports()
        return [(p.device, p.description) for p in ports]

    def auto_detect_arduino_port(self) -> Optional[str]:
        """Tries to find a likely Arduino port based on device description."""
        ports = serial.tools.list_ports.comports()
        keywords = ["arduino", "ch340", "ch341", "cp210", "ftdi", "usb serial", "usb-serial", "atmega"]
        for p in ports:
            desc = (p.description + " " + p.manufacturer if p.manufacturer else p.description).lower()
            if any(k in desc for k in keywords):
                return p.device
        # If no explicit keyword matches, return first COM port that is not bluetooth or SOL if possible
        candidates = [p.device for p in ports if "bluetooth" not in p.description.lower() and "sol" not in p.description.lower()]
        if candidates:
            return candidates[0]
        return ports[0].device if ports else None

    def connect(self, port: Optional[str] = None) -> bool:
        """Connects to the specified port or auto-detected port."""
        self.disconnect()

        target_port = port or self.auto_detect_arduino_port()
        if not target_port:
            self.connection_status = "NO COM PORTS DETECTED"
            return False

        try:
            self.connection_status = f"CONNECTING TO {target_port}..."
            self.serial_inst = serial.Serial(target_port, self.baud_rate, timeout=0.1)
            time.sleep(1.8) # Allow Arduino bootloader reset to settle
            self.current_port = target_port
            self.is_connected = True
            self.connection_status = f"CONNECTED ({target_port})"
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._read_worker, daemon=True)
            self.thread.start()
            return True
        except Exception as e:
            self.connection_status = f"ERR: {str(e)[:24]}"
            self.is_connected = False
            self.serial_inst = None
            return False

    def disconnect(self):
        """Disconnects serial port and stops worker."""
        self.stop_event.set()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=0.3)
        if self.serial_inst and self.serial_inst.is_open:
            try:
                self.serial_inst.close()
            except Exception:
                pass
        self.serial_inst = None
        self.is_connected = False
        self.connection_status = "DISCONNECTED"

    def send_command(self, cmd: str):
        """Sends a text command to Arduino."""
        if self.is_connected and self.serial_inst and self.serial_inst.is_open:
            try:
                msg = (cmd.strip() + "\n").encode("utf-8")
                self.serial_inst.write(msg)
            except Exception:
                pass

    def _read_worker(self):
        """Background thread that continuously reads lines from serial."""
        while not self.stop_event.is_set() and self.serial_inst and self.serial_inst.is_open:
            try:
                line = self.serial_inst.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    parsed = self._parse_line(line)
                    if parsed:
                        if self.rx_queue.full():
                            try:
                                self.rx_queue.get_nowait()
                            except queue.Empty:
                                pass
                        self.rx_queue.put(parsed)
            except serial.SerialException:
                self.is_connected = False
                self.connection_status = "CONNECTION LOST"
                break
            except Exception:
                time.sleep(0.01)

    def _parse_line(self, line: str) -> Optional[Tuple[int, float, bool]]:
        """Parses a serial line into (angle_deg, distance_cm, is_valid)."""
        # Try key-value format (angle_deg: X, distance_cm: Y)
        m = self.re_keyval.search(line)
        if m:
            try:
                ang = int(m.group(1))
                dist_str = m.group(2).lower()
                if "out" in dist_str:
                    return ang, -1.0, False
                dist = float(dist_str)
                return ang, dist, (2.0 <= dist <= 400.0)
            except ValueError:
                pass

        # Try CSV format (45, 23.4)
        m2 = self.re_csv.search(line)
        if m2:
            try:
                ang = int(m2.group(1))
                dist_str = m2.group(2).lower()
                if "out" in dist_str or dist_str == "-1":
                    return ang, -1.0, False
                dist = float(dist_str)
                return ang, dist, (2.0 <= dist <= 400.0)
            except ValueError:
                pass

        return None

    def get_latest_sample(self) -> Optional[Tuple[int, float, bool]]:
        """Retrieves the newest sample, clearing backlog."""
        last_item = None
        while not self.rx_queue.empty():
            try:
                last_item = self.rx_queue.get_nowait()
            except queue.Empty:
                break
        return last_item

