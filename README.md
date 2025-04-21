Sure! Here's your updated and clean `README.md` file — clearly documenting everything you've done so far in **English**, so it’s clear for judges, teammates, or contributors:

---

### ✅ `README.md`

```markdown
# WRO 2025 Future Engineers — Autonomous Car Project

This repository contains the software architecture and control code for our WRO 2025 Future Engineers robot car. The goal is to develop a fully autonomous vehicle that can navigate a track, avoid obstacles, and perform parking maneuvers using a modular, sensor-driven system.

---

## 🚗 Current Setup

### ✅ Hardware Configuration
- **Raspberry Pi 4** with Build HAT
- **LEGO Spike Motors:**
  - Port A: Rear drive motor (direct connection to both rear wheels)
  - Port B: Front steering motor (controls the rack-and-pinion steering)
- **Ultrasonic Sensors:**
  - Port C: Left distance sensor
  - Port D: Right distance sensor
- **USB Camera**:
  - Used for obstacle and parking zone detection
  - Connected via `/dev/video0`

---

## 📦 Code Architecture

### `/drive`
- `motors.py` — Controls forward/backward movement (rear motor)
- `steering.py` — Handles smooth left/right steering with max ±30° range

### `/sensors`
- `ultrasonic_left.py` / `ultrasonic_right.py` — Read and filter distance values for wall detection and avoidance

### `/vision`
- `camera_usb.py` — Initializes and reads from the USB camera
- `obstacle_detection.py` — Detects red/green vertical pillar-shaped obstacles using color and contour shape filters
- `parking_detection.py` — Detects a purple parking zone using color masks

### `/routines`
- `test_drive.py` — Tests motors, sensors, and camera in one script
- `main_run.py` — (To be implemented) Final logic for obstacle avoidance and parking

### Root Files
- `main.py` — Entry point that reads `mode.txt` and runs selected mode:
  - `main` → main autonomous routine
  - `test` → test all modules
- `mode.txt` — File-based mode selector (`main` or `test`)
- `config.py` — Centralized configuration for speeds, angles, sensor thresholds

---

## 🧪 How to Test the Robot

1. Set testing mode:
   ```bash
   echo "test" > mode.txt
   ```

2. Run the system:
   ```bash
   python3 main.py
   ```

3. The test sequence will:
   - Move forward and backward
   - Turn left and right (with limit angles)
   - Print distances from both ultrasonic sensors
   - Open the camera and show a real-time feed
   - Detect obstacles (red/green) and parking zones (purple)

---

## 🧠 Notes for Future Development

- Main logic will be driven by ultrasonic + camera combo:
  - **Obstacle avoidance**: if one side sees wall and the other doesn’t → turn
  - **Obstacle type**: red = avoid right, green = avoid left
  - **Parking detection**: triggered only during the last lap
- All control logic and parameters are fully configurable from `config.py`

---

## 👨‍🔧 Authors
- Contributors: Tair Qaldybayev and Ulan Gauan
