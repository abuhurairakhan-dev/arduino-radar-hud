# Contributing to the Arduino Ultrasonic Radar & Sci-Fi HUD Project

Thank you for your interest in contributing to this project! We welcome contributions to both the Arduino embedded firmware and the Python Sci-Fi HUD visualizer.

---

## Code of Conduct

Please be respectful and constructive in all issue discussions, code reviews, and communications.

---

## Getting Started

1. **Fork the Repository** to your GitHub account.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/arduino-ultrasonic-radar-system.git
   cd arduino-ultrasonic-radar-system
   ```
3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Test in Simulation Mode** (no hardware needed):
   ```bash
   python radar_scifi_hud.py --sim
   ```

---

## Guidelines for Contributions

### 1. Arduino Firmware (`arduino_radar/` and `src/`)
* **Timing Integrity**: Maintain non-blocking execution using `millis()`. Never introduce blocking `delay()` calls in the main loop.
* **Ultrasonic Safeguards**: Keep `SCAN_STEP_INTERVAL_MS >= 60` to respect the HC-SR04 transducer settling cycle.
* **Protocol Consistency**: Any modifications to the telemetry format emitted over serial must remain backward-compatible with `SerialManager._parse_line()` in `radar_visualizer/serial_comm.py`.
* Ensure changes are mirrored across both `arduino_radar/arduino_radar.ino` (Arduino IDE) and `src/main.cpp` (PlatformIO).

### 2. Python Sci-Fi HUD (`radar_visualizer/`)
* **Thread Safety**: Never interact with Pygame surfaces or UI elements from the serial background thread; pass all telemetry through thread-safe queues.
* **Zero External Audio Assets**: Procedural sound effects are synthesized mathematically in `audio.py` using NumPy. Avoid adding large audio binary files.
* **High Performance**: Maintain 60 FPS rendering by caching surfaces and avoiding redundant per-frame allocations.

---

## Submitting Pull Requests

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes with clear, descriptive commit messages.
3. Verify that the simulation runs without errors:
   ```bash
   python radar_scifi_hud.py --sim
   ```
4. Push your branch to GitHub and open a Pull Request against the `main` branch.

