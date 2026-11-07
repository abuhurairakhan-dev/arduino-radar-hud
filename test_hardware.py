#!/usr/bin/env python3
"""
Real Hardware Tester & Live Telemetry Inspector
Tests physical Arduino Uno + HC-SR04 + SG90 Servo + LED + Buzzer setup.
"""

import sys
import time
import re
import serial
import serial.tools.list_ports

def list_ports():
    return list(serial.tools.list_ports.comports())

def wait_for_arduino(timeout_sec=30):
    print("=" * 70)
    print("   NEXUS-7 REAL HARDWARE DIAGNOSTIC & CIRCUIT VERIFICATION TOOL")
    print("=" * 70)
    print("\n[Step 1] Detecting Arduino USB connection...")
    
    ports = list_ports()
    initial_ports = {p.device for p in ports}
    
    # Check if an Arduino-like device is already present
    for p in ports:
        desc = (p.description + " " + (p.manufacturer or "")).lower()
        if any(k in desc for k in ["arduino", "ch340", "ch341", "cp210", "ftdi", "usb serial", "usb-serial", "atmega"]):
            print(f"[FOUND] Detected Arduino on {p.device} ({p.description})")
            return p.device

    print("\n>> Searching for available COM ports...")
    valid_ports = [p for p in ports if "sol" not in p.description.lower() and "bluetooth" not in p.description.lower()]
    if valid_ports:
        print("Available candidate ports:")
        for idx, p in enumerate(valid_ports):
            print(f"  [{idx + 1}] {p.device}: {p.description}")
        choice = input(f"\nSelect port [1-{len(valid_ports)}] or press Enter to wait for USB plug-in: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(valid_ports):
            return valid_ports[int(choice) - 1].device

    print("\n>> Please plug your Arduino Uno into your computer's USB port now...")
    print("   (Watching for new COM port... Press Ctrl+C to cancel)\n")
    
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        current_ports = list_ports()
        for p in current_ports:
            if p.device not in initial_ports:
                print(f"\n[CONNECTED!] New USB device detected: {p.device} ({p.description})")
                return p.device
        time.sleep(0.5)

    print("\n[WARNING] No new port detected within timeout.")
    if ports:
        print("Existing ports:")
        for p in ports:
            print(f"  - {p.device}: {p.description}")
        manual = input("\nEnter COM port manually (e.g. COM3) or 'q' to quit: ").strip().upper()
        if manual.startswith("COM"):
            return manual
    return None

def test_hardware(port, baud=115200):
    print(f"\n[Step 2] Connecting to {port} at {baud} baud...")
    try:
        ser = serial.Serial(port, baud, timeout=1.0)
        time.sleep(2.0) # Wait for Arduino auto-reset
        print("[SUCCESS] Serial port opened successfully!\n")
    except Exception as e:
        print(f"[ERROR] Could not open {port}: {e}")
        print("\nTroubleshooting tips:")
        print("  1. Ensure Arduino IDE Serial Monitor is CLOSED (only one app can use the COM port at a time).")
        print("  2. Ensure code from src/main.cpp has been uploaded to the Arduino Uno.")
        print("  3. Check USB cable connection.")
        return False

    print("=" * 70)
    print("   LIVE SENSOR TELEMETRY & CIRCUIT VERIFICATION")
    print("   Wave your hand in front of the HC-SR04 sensor to test distance!")
    print("=" * 70)
    print(f"{'TIMESTAMP':<10} | {'SERVO ANGLE':<12} | {'DISTANCE':<14} | {'STATUS':<20} | {'ALARM'}")
    print("-" * 70)

    # Send TEST command to verify LED & Buzzer
    try:
        ser.write(b"TEST\n")
    except Exception:
        pass

    re_data = re.compile(r"angle(?:_deg)?\s*:\s*(\d+).*?distance(?:_cm)?\s*:\s*([\d\.]+|out_of_range)", re.IGNORECASE)

    sample_count = 0
    readings = []

    try:
        start = time.time()
        while sample_count < 40:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            m = re_data.search(line)
            if m:
                sample_count += 1
                angle = int(m.group(1))
                dist_str = m.group(2)
                t_str = f"+{time.time() - start:.1f}s"

                if "out" in dist_str.lower():
                    dist_val = -1.0
                    status = "Out of range"
                    alarm_str = "OFF"
                    d_disp = "--.- cm"
                else:
                    dist_val = float(dist_str)
                    readings.append(dist_val)
                    d_disp = f"{dist_val:5.1f} cm"
                    if dist_val <= 30.0:
                        status = ">> PROXIMITY ALERT <<"
                        alarm_str = "[ACTIVE (LED+BUZZ)]"
                    else:
                        status = "Tracking target"
                        alarm_str = "OFF"

                bar_len = min(25, max(0, int(dist_val / 2.0))) if dist_val > 0 else 0
                dist_bar = "[" + "=" * bar_len + " " * (25 - bar_len) + "]" if dist_val > 0 else "[ NO ECHO DETECTED ]"

                print(f"{t_str:<10} | {angle:3d} deg      | {d_disp:<14} | {status:<20} | {alarm_str}")

    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        ser.close()

    print("\n" + "=" * 70)
    print("   HARDWARE DIAGNOSTIC SUMMARY")
    print("=" * 70)
    if sample_count > 0:
        print(f"[OK] Total telemetry packets received: {sample_count}")
        if readings:
            min_d = min(readings)
            max_d = max(readings)
            print(f"[OK] Ultrasonic sensor is ACTIVE! Measured range: {min_d:.1f} cm to {max_d:.1f} cm.")
            if min_d <= 30.0:
                print("[OK] Proximity alarm threshold (<30cm) was successfully triggered!")
            else:
                print("[NOTE] Place an object closer than 30cm to test the LED & Buzzer alarm.")
        else:
            print("[NOTE] Sensor only reported 'out_of_range'. Check if TRIG and ECHO wires are firmly connected.")
        return True
    else:
        print("[FAIL] No valid telemetry packets received.")
        print("Please check: Did you upload src/main.cpp using Arduino IDE at 115200 baud?")
        return False

def main():
    port = None
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = wait_for_arduino()

    if not port:
        print("\nExiting. Run again when Arduino is plugged in.")
        return

    success = test_hardware(port)
    if success:
        print("\nCircuit test completed!")
        ans = input("\nDo you want to launch the Sci-Fi HUD Visualizer now? (Y/n): ").strip().lower()
        if ans in ("", "y", "yes"):
            import subprocess
            subprocess.run([sys.executable, "radar_scifi_hud.py", "--port", port])

if __name__ == "__main__":
    main()

