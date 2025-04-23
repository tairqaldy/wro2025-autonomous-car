# WRO2025 Autonomous Car EngineeringJournal

## Project Overview

The **WRO 2025 Autonomous Car** project is a self-driving robotic vehicle built for the World Robot Olympiad 2025 Future Engineers challenge. The goal is to navigate a model car through a dynamically changing track **autonomously** – following walls, detecting road signs/markers to make turns, avoiding obstacles, and performing a parallel parking at the finish. This repository contains all the code and documentation for our team's autonomous car, including driving control, sensor integration, and computer vision for obstacle and parking detection.

**Key Features:**

- **Autonomous Navigation:** The robot uses dual distance sensors to follow the left wall of the track and maintain a target distance, adjusting steering in real-time. It detects when to make left or right turns using color markers (or “road signs”) on the course.
- **Obstacle Avoidance:** Using a vision system (Limelight 3A camera), the car identifies obstacle pillars on the track and decides whether to bypass them on the left or right side.
- **Parallel Parking Maneuver:** At the end of the run, the robot searches for a designated parking zone marker and performs a parallel parking sequence autonomously.
- **Mode Selection:** Operation modes (test, speed run, main competition run, etc.) can be selected via a simple text file or command-line argument, allowing easy switching between a full autonomous run, a speed-focused run (laps without obstacles), or testing routines.
- **Logging and Debugging Aids:** The code includes detailed logging (in both console and `run.log`) to help diagnose issues with sensors or actuators during development and runs.

This README provides an overview of the hardware setup, wiring, installation, and usage instructions, as well as troubleshooting tips and notes on limitations. An accompanying **Engineering Journal** (see bottom of this document) chronicles the development process, design decisions, and lessons learned by the team.

## Hardware Used

Our autonomous car integrates several hardware components. Below is a list of the key hardware elements used in the project and their roles:

- **Raspberry Pi 4B (4GB)** – The main controller running the robot’s software (Python code). We chose the Pi 4 for its processing power to handle sensor input and computer vision (OpenCV) for the camera.
- **Raspberry Pi Build HAT** – An add-on board for the Pi used to interface with LEGO Technic motors and sensors. This board contains a microcontroller that communicates with the Pi over serial (UART) and provides 4 ports (labeled A, B, C, D) for LEGO motors/sensors. It simplifies control of our motors and distance sensors.
- **Drive Motor** – A DC motor responsible for rear-wheel drive. In our final build, this is a LEGO Technic medium motor connected to Build HAT port **A** (allowing precise speed control via the Build HAT library). In earlier iterations, we used a hobby DC motor driven by an L298N H-bridge driver.
- **Steering Motor** – A motor for front-wheel steering. We use a LEGO Technic angular motor on Build HAT port **B** to actively turn the front wheels. This motor is controlled to specific angles (acting similarly to a servo for steering). *(In a previous design, we had a standard hobby servo for steering; the switch to a LEGO motor via Build HAT improved reliability in the final design.)*
- **Distance Sensors (x2)** – Two Time-of-Flight distance sensors for wall following (similar to VL53L0X modules). In the final configuration, we attached two LEGO SPIKE Prime Distance Sensors (which internally use IR time-of-flight) to ports **C** (left side) and **D** (right side) of the Build HAT. These provide distance readings in millimeters to detect the distance to the wall on each side. *(Originally, we experimented with two VL53L0X breakout sensors directly via I2C – see Engineering Journal for how we resolved address conflicts.)*
- **Limelight 3A Camera** – A smart USB camera used for vision processing. The Limelight 3A (an FRC vision camera) is connected to the Pi via USB and serves as our forward-facing camera. We leverage it to detect colored obstacles (red/green pillars) and the parking zone markers. We primarily use it as a standard USB camera in our code (capturing frames with OpenCV), although the Limelight’s internal processing can also be used for tuning and visualization during development.
- **Power Supply** – A dedicated power source for motors and electronics. The Raspberry Pi and Build HAT are powered by a rechargeable battery pack. In our setup, an 8x AA NiMH battery pack (approx. 9.6V) connects to the Build HAT’s power input, which in turn powers the LEGO motors and sensors. The Pi itself is powered either through the Build HAT or its USB-C port (from the same battery via a DC-DC regulator ensuring 5V). This allows the robot to operate untethered on the track. *(In earlier versions, the L298N and DC motor were driven by a 7.4V Li-ion battery while the Pi was powered by a USB power bank.)*

 ([image]()) *Our autonomous car robot (final version) featuring the Raspberry Pi 4B (center), connected to sensors and motors. The Build HAT is mounted under the Pi to interface with LEGO motors (for drive and steering) and distance sensors. Visible at the front is the Limelight 3A camera (black box), and at the rear-right is a power management module.* 

## Circuit and Pin Mappings

Understanding the wiring and pin connections is crucial for replication and troubleshooting. Below we describe how each component is connected in our final configuration:

 ([image]()) *Raspberry Pi 4B GPIO pinout with our connections annotated. We utilized the Build HAT for most sensor/motor connections, which communicates via the Pi’s UART (TX/RX pins). Separate I2C buses were used when testing dual VL53L0X sensors.* 

- **Raspberry Pi to Build HAT:** The Build HAT attaches directly to the Pi’s 40-pin header. Communication between the Pi and Build HAT uses the UART pins (GPIO 14 TXD and GPIO 15 RXD) internally. These pins carry a serial protocol that the Build HAT’s microcontroller uses to control motors and read sensors. The Build HAT also takes 5V and 3.3V from the Pi for logic power and provides power to motors via an external supply. (If using the Build HAT as we did finally, ensure the Pi’s UART is enabled and not used for console, since it’s needed by the Build HAT.)
- **Build HAT Ports:** 
  - Port **A** – Connected to the **rear drive motor** (LEGO motor). In code, this is initialized as `Motor('A')`. This port drives the car forward or backward by powering the motor in either direction.
  - Port **B** – Connected to the **steering motor** (LEGO motor for front steering). Initialized as `Motor('B')`. We use the Build HAT’s ability to run the motor to specific positions (angles) to steer left/right. The motor is mechanically linked to turn the front wheels.
  - Port **C** – Connected to the **left distance sensor** (LEGO Distance Sensor). In code, `DistanceSensor('C')` reads the distance to the left wall. This sensor faces left side of the vehicle.
  - Port **D** – Connected to the **right distance sensor** (LEGO Distance Sensor). In code, `DistanceSensor('D')` for the right side distance. (The right sensor is mainly used in the high-speed mode for detecting lost wall on the right side.)
- **Limelight 3A Camera:** The Limelight is connected via USB to the Raspberry Pi. It enumerates as a USB camera (`/dev/video*`). We did not use any special GPIO pins for the camera. The camera also supports an Ethernet-over-USB interface (with a static IP like 172.29.0.1 and a web dashboard at `limelight.local:5801` as seen in development), but for simplicity our code uses OpenCV to grab frames from it like a standard webcam.
- **I2C Buses (when using custom sensors):** Initially, for two VL53L0X ToF sensors, we configured one on the Pi’s default I2C-1 bus (GPIO 2 SDA1, GPIO 3 SCL1) and the other on the secondary I2C-0 bus (GPIO 0 SDA0, GPIO 1 SCL0). This was done to avoid address conflicts since both sensors have the same default address. Each sensor got 3.3V power (pin 1 or 17) and Ground (pin 6 or 9). By enabling I2C-0 (typically reserved for HAT EEPROM) in Raspberry Pi settings, we could use two separate I2C channels for the two sensors. **Note:** In the final build, we moved to LEGO distance sensors via the Build HAT, so this dual-bus solution was no longer needed, but it’s a viable approach if using the VL53L0X modules without a Build HAT.
- **Optional Servo (earlier version):** If using a standard servo for steering (earlier design), we used GPIO 13 (PWM1) for the servo control signal, 5V (pin 2) for servo power, and a ground pin (pin 6) for common ground. GPIO 13 is a hardware PWM-capable pin which can drive servo pulses with better timing. (In code, this was handled via the `pigpio` library in tests, but in final code we removed servo control in favor of the Build HAT motor.)
- **L298N Motor Driver (earlier version):** The dual H-bridge was used when controlling a DC drive motor directly. It was connected to:
  - Two GPIOs for direction control (IN1, IN2 of the H-bridge).
  - One GPIO with PWM for speed control (EN/A pin of H-bridge).
  - 12V battery input to the L298N’s VS (or 7.4V Li-ion in our case) and ground tied with the Pi ground.
  - Motor output from L298N to the drive motor terminals.
  We have omitted these connections in the final setup since the Build HAT and LEGO motor replaced this system. If needed, ensure to disable the Build HAT overlay and instead use a library like RPi.GPIO or `gpiozero` for motor control.

**Wiring Diagram Summary:** The Raspberry Pi with the Build HAT controls all motors/sensors through the Build HAT ports, minimizing direct GPIO wiring. The only direct connections to the Pi’s GPIO in the final design are the UART to the Build HAT (through the header) and the I2C (which ended up not being used after switching to Build HAT sensors). This simplified the wiring and reduced potential issues. Always double-check that the external power supply for motors (Build HAT power input or L298N VIN) shares a common ground with the Raspberry Pi to avoid inconsistent sensor readings or control signals.

## Installation & Setup Instructions

To replicate or run this project, you need to set up the software environment on the Raspberry Pi and ensure all libraries are installed. Below are the steps and requirements:

**1. Operating System:**  
We used **Raspberry Pi OS (32-bit)**, based on Debian, updated as of early 2025. Ensure your OS is up-to-date and enable the interfaces for serial (UART) and I2C via `raspi-config`. Specifically:
   - Enable the serial interface for the Build HAT. Disable the serial console (so the UART is free for the Build HAT to use).
   - Enable I2C (for any I2C sensors or the Build HAT’s detection of ID EEPROM, etc.).

**2. Python Environment:**  
Python 3 is used (the code is tested with Python 3.9+). Clone or download this repository to your Raspberry Pi. We recommend using a Python virtual environment for the project:
```bash
git clone https://github.com/yourusername/wro2025-autonomous-car.git
cd wro2025-autonomous-car
python3 -m venv venv
source venv/bin/activate
```

**3. Required Libraries:**  
Install the required Python libraries using pip. All dependencies are listed in `requirements.txt`. You can install them with:
```bash
pip install -r requirements.txt
```
Key libraries include:
   - **BuildHAT** – Official Raspberry Pi Build HAT library (`pip install buildhat`). This provides the `Motor` and `DistanceSensor` classes used in our code.
   - **OpenCV** – For camera input and image processing (`opencv-python` package). Make sure this installs correctly on Raspberry Pi (it can be heavy; alternatively use `sudo apt install python3-opencv`).
   - **NumPy** – Required by OpenCV and used for image processing.
   - **RPi.GPIO or pigpio** – (If using servo or custom motor driver in any tests) RPi.GPIO is usually pre-installed. We primarily rely on BuildHAT library for motor control, so GPIO usage is minimal in final code.
   - **(Optional) imutils** – If any image utility functions are used (not critical).
   - **logging** – Python’s logging is used; no need to install, part of standard library.
   - **cv2FRC (Limelight)** – *Note:* The Limelight 3A can stream to NetworkTables if using WPILib. We did not use NetworkTables in this project, so no FRC-specific libraries are needed. We treat it as a generic USB camera.

After installing, ensure the Build HAT firmware is up to date. The first time you run a BuildHAT script, it may flash the latest firmware to the HAT. Just run a small test like:
```python
from buildhat import Motor
m = Motor('A')
```
If it initializes without error, your Build HAT is ready.

**4. Hardware Setup:**  
- Mount the Build HAT on the Raspberry Pi’s GPIO header (if using it). Connect the LEGO motors and sensors to the designated ports (A, B, C, D as per our mapping above).
- Supply power to the Build HAT (per its specs, 8V-12V recommended; we used ~9V). The Pi can be powered via the HAT or separately. 
- Connect the Limelight camera to a USB port on the Pi. If using a different USB camera, adjust `config.py` for the correct device index (our default is `/dev/video10` which was the Limelight’s enumerated path).
- (If using alternative hardware) Connect the servo and motor driver as per Circuit section and adjust code where necessary (e.g., replacing BuildHAT motor calls with servo control code).

**5. System Configuration:**  
- **Autostart (optional):** If you want the robot code to run on boot (e.g., in competition), you might set up a systemd service or `cron @reboot` to launch a particular mode. We did not include that in this repo, but it can be set up after testing.
- **Camera Focus/Exposure:** The Limelight has a fixed focus (infinite) and adjustable exposure via its interface. We manually tuned exposure and gain through the Limelight web interface to work in our lighting conditions (ensuring the colored objects are distinguishable). If using a normal webcam, you might need to adjust OpenCV capture settings (e.g., `cv2.VideoCapture.set()` for exposure).

With hardware wired and software installed, you’re ready to run the code. 

## Code Structure and Usage

The repository is organized into modules by functionality for clarity. Here’s an overview of the structure and how to use the code:

```plaintext
wro2025-autonomous-car/
├── main.py               # Main entry script to select mode and start the appropriate routine
├── mode.txt              # Text file that specifies which mode to run (test, speed, main, etc.)
├── config.py             # Configuration constants (speeds, angles, thresholds, etc.)
├── drive/
│   ├── motors.py         # Functions to control the drive motor (forward, backward, stop)
│   └── steering.py       # Functions to control the steering motor (left, right, straight)
├── sensors/
│   ├── ultrasonic_left.py    # Interface to left distance sensor (via BuildHAT DistanceSensor 'C')
│   └── ultrasonic_right.py   # Interface to right distance sensor (via BuildHAT DistanceSensor 'D')
├── vision/
│   ├── camera_usb.py         # Camera initialization and frame capture using OpenCV
│   ├── obstacle_detection.py # Functions to detect obstacle (pillar) and decide bypass direction
│   └── parking_detection.py  # Functions to detect the parking zone markers
├── routines/
│   ├── test_drive.py         # Routine to test basic driving (motor and steering) 
│   ├── camera_only.py        # Routine to test only the camera feed and vision processing
│   ├── speed_run.py          # Routine for speed mode (laps without obstacle navigation)
│   ├── main_run.py           # Routine for full autonomous run (obstacles + parking)
│   └── test_obstacle_camera.py # Routine to visualize obstacle detection with camera
└── EngineeringJournal.md     # The engineering log (development journal)
```

Key scripts and how to use them:

- **main.py:** This is the primary entry point. It reads the `mode.txt` file (or can parse a command-line argument) to decide which routine to run. To use it, set the desired mode in `mode.txt` (e.g., write `main` for the full autonomous run) and then execute:
  ```bash
  python3 main.py
  ```
  Alternatively, you can pass the mode as an argument and skip using the file, for example:
  ```bash
  python3 main.py speed
  ```
  Available modes:
  - `test` – Runs a comprehensive test of all components (motors, sensors, camera, etc.) in sequence. This is useful to verify everything is working.
  - `speed` – Runs the **Speed Run** mode, where the car drives laps quickly without performing obstacle avoidance or parking. It will still use the distance sensors to stay centered in the lane (detecting loss of left/right wall).
  - `camera` – Runs a camera test, which simply initializes the camera and streams frames or does a specific vision test (like detecting colored markers in real-time).
  - `main` – Runs the full **Competition Mode**: the car will use turn detection, obstacle avoidance, and parking logic to attempt the complete challenge.
  
  If `mode.txt` is not found, the program defaults to `test` mode with a warning. If an unknown mode is set, it will exit with an error.

- **config.py:** Contains tunable parameters for the robot’s behavior. For example:
  - Speed settings (DEFAULT_SPEED, DRIVE_SPEED for the motors),
  - Steering angles (MAX_TURN_ANGLE for how far wheels turn, STRAIGHT_ANGLE offset if any for straight),
  - Distance targets (TARGET_DISTANCE_MM is the desired gap to the wall for wall-following),
  - Lap settings (TURNS_PER_LAP, TOTAL_LAPS if we restrict how many laps the robot does before stopping),
  - Delays (TURN_DELAY to wait after completing a turn, WALL_CORRECTION_DELAY for how frequently to adjust steering for wall, PARKING_DELAY between parking maneuvers),
  - Camera settings (CAMERA_INDEX, frame width/height if needed by OpenCV),
  - DEBUG_MODE flag (if true, logging level is set to DEBUG for more verbose output, otherwise INFO).
  
  You can modify these constants to fine-tune performance. For instance, increasing `DEFAULT_SPEED` will make the car drive faster, but be cautious as higher speeds may cause missed turn detection or unstable wall following if not tuned.

- **motors.py (Drive Motor Control):** Provides `drive_forward(speed, duration)` and `drive_backward(speed, duration)` functions to move the car. These use the Build HAT Motor on port A. If a `duration` (seconds) is provided, the function will run the motor for that time and then stop. Otherwise, it will run indefinitely (until stopped by another call). `stop_all()` stops the drive motor. The default speed is set by `DRIVE_SPEED` in config (a percentage of max power, 100 is full speed). Positive speed drives forward, negative drives backward.

- **steering.py (Steering Control):** Manages the steering motor (Build HAT Motor on port B). Functions:
  - `steer_left()` – turn the front wheels left by running the motor to `-MAX_TURN_ANGLE` then returning to center.
  - `steer_right()` – similarly, turn right to `+MAX_TURN_ANGLE` then back to center.
  - `steer_straight()` – return wheels to the straight position (angle 0).
  
  These use the motor’s positional control: `steering_motor.run_to_position(angle)` with a certain speed. A short delay (0.3s) is used to allow the movement to complete before continuing. For example, `MAX_TURN_ANGLE` is 25 degrees in our config, so calling `steer_left()` turns the wheels 25° to the left and then straightens them. We print some debug info (e.g., current steering angle) for feedback. The steering motor is calibrated such that 0° corresponds to wheels roughly straight ahead.

- **ultrasonic_left.py & ultrasonic_right.py (Distance Sensors):** Provide `get_distance_left()` and `get_distance_right()` functions. These read the distance sensor multiple times and return an averaged distance in millimeters. They use the Build HAT’s `DistanceSensor` class which returns distance or -1 if out of range/no object. By sampling a few times (default 3 samples) and ignoring -1 readings, we smooth out noise. The functions return -1 if no valid reading (meaning the sensor might not see a wall within range). These are used for wall-following: if left sensor returns -1, it implies no wall on the left (maybe a left turn or open area), similarly for right.

- **camera_usb.py:** Handles camera initialization using OpenCV. It sets up the video capture with the index specified in `config.py` (by default `/dev/video10` for Limelight). Functions:
  - `init_camera()` – tries to connect to the camera and set resolution (640x480) and returns True if successful.
  - `capture_frame()` – grabs a frame from the camera (as a NumPy array image).
  - `release_camera()` – releases the capture device when done.
  
  If the camera is not found or cannot capture, these functions will print an error or return None. We use these in vision-based routines to get images for processing.

- **vision/obstacle_detection.py:** Contains logic to detect obstacle pillars in the camera frame and decide which side to pass them. The approach:
  - Convert the captured frame from BGR to HSV color space.
  - Create color masks for red and green (the expected colors of the obstacle markers):
    - Red mask: we actually combine two ranges (to capture red hues around 0° and 360° in HSV). We threshold on HSV to detect red areas, then apply some blurring.
    - Green mask: threshold for green hue range.
  - Use contour detection on these masks to find the colored objects (likely the pillars).
  - Determine the position of the pillar relative to the center of the image (or robot). We categorize an obstacle as on the left or right side based on which half of the camera frame the contour is detected, and possibly its color.
  
  The function `analyze_obstacle()` (called in autonomous runs) returns `"left"`, `"right"`, or `None`:
   - `"left"` means the robot should veer left (likely an obstacle is detected on the right side of the path, so going left avoids it).
   - `"right"` means veer right (obstacle on left side).
   - `None` means no obstacle detected ahead or it’s safe to continue straight.
  
  There is also a helper `detect_pillar_in_mask(mask, color_name)` that finds contours of a given color mask and annotates the frame (for debugging). This is used in `test_obstacle_camera.py` to show detection results live. 

- **vision/parking_detection.py:** Contains `detect_parking_zone()` which processes the camera image to find the parking zone markers. In WRO, the parking zone might be indicated by specific markers (for example, two AprilTags or colored strips). Our approach (simplified due to time constraints) was to look for a particular color or shape at the end of the run. We assumed the parking zone might have a unique color marker (perhaps blue or black tape rectangle). The function returns True if the parking zone is found in the current frame. In the `main_run` sequence, we use this in a loop to slowly creep forward until the parking zone is detected, then stop and finalize parking.

- **routines/test_drive.py:** A simple routine to verify movement. It might drive forward a short distance, steer left/right, etc., to confirm motors are responding correctly. (This was primarily used early in development to ensure our motor wiring and directions were correct.)

- **routines/test_obstacle_camera.py:** When run, this will open a window showing the camera feed with colored obstacle detection overlays. It continuously captures frames, applies the red/green mask detection, draws bounding boxes on any detected pillars, and displays the result. Press `q` to quit the loop. This was used to fine-tune the vision algorithms for obstacle detection.

- **routines/speed_run.py:** This script implements a **speed run mode** where the goal is to complete laps as fast as possible (ignoring obstacle avoidance and parking). In this mode, the robot basically drives straight for a fixed short duration, then stops and checks the distance sensors:
  - It prints the left and right distances for debug.
  - If the left wall is lost (`left == -1`), it assumes there’s a left turn (or it drifted away from left wall) and steers left slightly to find the wall again.
  - If the right wall is lost, it steers right.
  - It then continues driving forward again. This way, even at higher speeds, if the robot loses sight of a wall, it corrects course. This loop continues indefinitely (or until a KeyboardInterrupt is sent).
  - *Note:* This mode doesn’t explicitly count laps or detect finish; it’s mainly for testing maximum speed on straight segments while still staying in bounds. Use with caution, as no turn markers are actively read – it relies on walls.

- **routines/main_run.py:** This is the full autonomous challenge routine combining everything:
  1. **Initialization:** Resets lap and turn counters, and tries to initialize the camera (if available). If the camera (Limelight) isn’t found, it logs a warning and proceeds without obstacle avoidance (meaning the robot will just drive and ignore obstacles/parking).
  2. **Main Loop (Navigation):** While laps completed < TOTAL_LAPS:
     - Check for turn signal using `check_turn_color()`. This function likely reads a color sensor or camera to determine if a left or right turn is indicated at the current position. If it returns "left" or "right":
       - The robot executes a turn maneuver by calling `turn_left()` or `turn_right()` (from `drive/turns.py` module – these would likely involve steering and possibly a short forward drive to complete the turn, combining motor and steering control).
       - Increment turn_counter, and if turn_counter >= TURNS_PER_LAP, increment lap_counter (meaning one full lap done) and reset turn_counter for next lap.
       - Print/log the turn and lap completion, then delay for TURN_DELAY seconds to stabilize after the turn.
       - Continue (go back to loop start to check next iteration).
     - If no turn is needed right now, the car will do wall-following by reading the left distance (`get_distance_left()`):
       - If distance == -1 (no wall detected on left), it means we might be at a gap or the wall ended (could be a left turn ahead or open area), so the code just drives forward (the assumption is that either it will find a wall again or a turn signal soon).
       - If distance > TARGET_DISTANCE_MM + tolerance, the car is too far from the left wall – it steers left a little (e.g., turn wheels left 5 degrees) while driving forward, to move closer to the wall.
       - If distance < TARGET_DISTANCE_MM - tolerance, the car is too close to the wall – it steers right a bit while moving, to give more space.
       - Otherwise (distance is in acceptable range), it keeps the wheels straight and drives forward.
       - These slight steering adjustments happen continuously (with a small delay WALL_CORRECTION_DELAY in between) to keep the vehicle roughly centered at the target distance from the wall.
     - This loop repeats, checking for turns and adjusting course. In parallel, if the camera is on and an obstacle appears, we would integrate `analyze_obstacle()` logic here (in a future improvement, we considered fusing that in the loop to decide to go around an obstacle if detected).
  3. **Obstacle Avoidance:** In our implementation, obstacle avoidance was partly handled by the turn logic or by manual intervention if the camera wasn’t working. Ideally, we would insert:
     ```python
     direction = analyze_obstacle()
     if direction == "left":
         # obstacle detected ahead, go around it from left side
         steer_left()
         time.sleep(0.5)
         steer_straight()
     elif direction == "right":
         # obstacle detected, go around from right
         steer_right()
         time.sleep(0.5)
         steer_straight()
     ```
     into the loop. In testing, we found the color detection of obstacles was working, but integrating that with wall-following required careful tuning to avoid false positives. We left this for a future iteration (or manual mode triggers).
  4. **Parking Sequence:** After the laps are completed, the code checks if the camera was available. If yes, it enters a parking search loop:
     - It drives forward slowly (`PARKING_SPEED`) for short bursts, each time capturing a frame and using `detect_parking_zone()` to look for the parking markers.
     - Once `found` is True, it stops and then drives forward a bit more into the zone to ensure the robot is fully in.
     - Logs that parking is successful and breaks out. If the camera was not available, it skips parking with a message.
  5. **Cleanup:** Regardless of what happens, the `finally` block stops all motors and releases the camera if it was in use.
  
  You can run this full routine via `main.py` mode "main". This is what would be used in the actual competition run.

- **drive/turns.py:** (Though not explicitly shown in the file tree screenshot above, our code references it.) This module contains higher-level turn maneuvers, combining drive and steering:
  - `turn_left()` – Likely implementation: steer wheels left, drive forward for a short duration to make the turn, then straighten.
  - `turn_right()` – Similarly for right turns.
  These functions would also possibly incorporate using the distance sensors to align with the new wall after turning (for example, a left turn could use the front sensor briefly or just a timed approach).
  In our final code, we simplified turning by relying on the physical track having guide lines; thus, our `steer_left()` + forward was sufficient in testing. However, these can be expanded to more sophisticated maneuvers if needed (like pivot in place vs smooth turn).

**Usage Example:** To do a full test of all components, ensure `mode.txt` contains `test` and run `python3 main.py`. This will:
  - Test driving forward and backward (you should see the car move a bit).
  - Test steering left/right (watch the wheels turn).
  - Read distances and print them.
  - Initialize camera and attempt a test capture (printing success or failure).
  - Attempt obstacle detection (printing out which side it thinks the obstacle is, if any).
  - Attempt parking zone detection (printing if found or not).
  - End with a message "All tests completed".

For an actual autonomous drive, put `main` in `mode.txt` and run `python3 main.py`. Make sure the robot is placed at the start of the track, aligned properly with the left wall, and that the camera can see the path ahead. The robot should start driving and handle the course on its own.

## Mode System (Using mode.txt)

We implemented a simple mode selection system to switch between different behaviors without needing to constantly modify code. The file `mode.txt` in the project directory is read by `main.py` on startup to determine what the robot should do. This makes it easy for team members or judges to change modes by editing the file (for example, via SSH or a keyboard on the Pi) rather than altering code.

- To change mode, open `mode.txt` in a text editor and write one of the supported modes (e.g., `speed` or `main` or `test`). Save the file.
- Then run the program. The `run_selected_mode()` function in `main.py` handles this. It tries to open `mode.txt`, reads the first word, and matches it to a mode.
- If the file is missing or empty, it will default to "test" mode and print a warning.
- If the mode is not recognized, it prints an error and exits.

The recognized modes (and their corresponding functions) are:
- **test** – Runs `routines.test_drive.run_all_tests()` (which sequentially calls tests as described above).
- **speed** – Runs `routines.speed_run.speed_run()` (a loop for fast lap running).
- **camera** – Runs `routines.camera_only.run_camera_test()` (or `test_obstacle_camera` depending on implementation; essentially tests the camera feed and obstacle detection without driving).
- **main** – Runs the full `routines.main_run.run_main_mode()` (...(continued from above)**main** – Runs the full `routines.main_run.run_main_mode()` (the complete autonomous routine with obstacle avoidance and parking).

Using `mode.txt` means non-programmers on the team can easily switch what the robot does by just editing a file, and it also allows the code to auto-select modes on boot (if set up) without needing different scripts. We included this to streamline testing various aspects (for example, setting mode to `camera` when focusing on vision tuning, then back to `main` for an integrated test).

## Troubleshooting

Despite careful planning, we encountered and addressed many issues. Here are some common problems and troubleshooting tips for this project:

- **Limelight Camera Not Detected:** If the camera fails to initialize (e.g., `init_camera()` returns False), first ensure it’s properly connected. Run `ls /dev/video*` to see if it appears (our Limelight showed up as `/dev/video10`). If not, try power-cycling the camera or using a powered USB hub (the Limelight can draw significant power). Also, check that no other process is using the camera. If using a different webcam, update `CAMERA_INDEX` in `config.py` (for example, common webcams might be `/dev/video0`). Another tip: use `fswebcam` or `v4l2-ctl --list-devices` to verify the camera feed outside our program. In case of exposure issues (image too dark/bright), adjust the Limelight settings via its web interface or use OpenCV to set exposure (some cameras allow `cap.set(cv2.CAP_PROP_EXPOSURE, value)`).

- **“Build HAT not found” / Motor not responding:** The Build HAT communicates via the Pi’s serial port. If motors and sensors aren’t initializing (e.g., `Motor('A')` hangs or throws an exception), ensure:
  - The Build HAT is firmly seated on the GPIO header.
  - UART is enabled and not occupied by the console. In `/boot/config.txt`, you might need `enable_uart=1` and remove any `console=serial0` from `/boot/cmdline.txt`.
  - Supply power to the Build HAT’s power input. The motors won’t move if the external supply is missing or too low, even though the Pi might power the logic. The status LED on the Build HAT should be green. If it’s red or off, check the supply.
  - Run the program as a privileged user. The BuildHAT library might need root access to control the hardware (if not, ensure the user is in the correct groups like `dialout` for serial).
  - If using an alternative motor driver instead of Build HAT, make sure to disable the Build HAT initialization in code and use the appropriate library (e.g., RPi.GPIO for L298N) – otherwise the code will wait for a Build HAT that isn’t there.
  
- **I2C Errors or Distance Sensor Issues:** If using the VL53L0X sensors on I2C, you **must address the I2C conflict**. By default, both will try to use address 0x29 and you’ll get erroneous readings or I/O errors. We solved this by using two I2C buses (see Circuit section). Alternatively, use the XSHUT pin on one sensor to programmatically change its address at start-up. Ensure I2C is enabled (`raspi-config`) and use `i2cdetect -y 1` (and `-y 0` for the second bus, if enabled) to see if the sensors are detected at distinct addresses. If you get `Remote I/O error` or `-1` readings frequently:
  - Check wiring (especially SDA/SCL and that each sensor has correct pull-ups, though the Pi has built-in pull-ups on I2C).
  - Ensure you aren’t trying to read both sensors on the same bus without changing one’s address.
  - Use our averaging approach to filter out occasional spurious -1 values.
  - If using LEGO distance sensors via Build HAT, these issues go away, as the Build HAT handles them internally. But if a Build HAT DistanceSensor returns -1 always, it might mean the sensor isn’t connected to the port you expect or the port letter is wrong.
  
- **Sensor Misreads / Noise:** Our distance sensors sometimes gave a sudden -1 (especially if the wall has a gap or very sharp angle to the sensor). We mitigated this by averaging and by the logic that treats -1 as “no wall, keep going straight.” If you find the robot occasionally swerves due to a blip in reading, consider increasing the sample count or adjusting `TARGET_DISTANCE_MM` and tolerance to be a range rather than a single value. Also ensure the sensors are aimed correctly (parallel to ground, directly toward the walls, at an appropriate height).

- **Oversteering or Unstable Steering:** If the car oscillates or over-corrects while wall-following, you may need to reduce the adjustment step (we used 5 degrees). This is essentially a P-control on error. You can also implement a simple P or PD controller to smooth it. Our mechanical setup had some play, so we limited the steering range. If using a servo, ensure the servo’s range is calibrated and you’re not commanding beyond its physical limit. If the car turns too sharply at corners and loses the line, consider slowing down (`DEFAULT_SPEED`) or adding a brief stop before turning to allow the sensor/logic to catch up.

- **Incorrect Turn Detection:** If the robot misses turns or turns at wrong times:
  - Verify the color sensing mechanism (`check_turn_color()`). If using a color sensor, test that it reliably distinguishes the turn marker colors from the floor. Adjust thresholds or sensor placement as needed (the sensor should be close enough to the surface).
  - If using the camera for turn signals, ensure the field of view and processing logic aligns with where the markers are. You might need to restrict the ROI (region of interest) to look at the lower part of the frame or a specific angle.
  - Lighting can affect color detection. We found using HSV color space helped. You may need to tune the HSV ranges for red/green in `obstacle_detection.py` if the ambient lighting is different.
  - The WRO rules often provide specific RGB values for markers – use those as a guide to tune detection.
  
- **PWM and Timing Issues (earlier design):** When we used RPi.GPIO to control a servo and motor driver, we encountered jitter and inconsistent speeds. This was due to software PWM limitations. If you go that route, consider using the `pigpio` daemon which generates hardware-timed PWM signals on any GPIO. Also, ensure that the frequency for the motor PWM is appropriate (e.g., 100Hz or higher for smooth motor control) and for servo ~50Hz. In our final Build HAT approach, these issues were resolved by offloading to the HAT. If you must troubleshoot PWM:
  - Check for conflicting pin usage (the Pi has only one hardware PWM channel on GPIO18 and another on GPIO19/13 if PCM is repurposed).
  - Close any libraries that might be controlling the same pins (for instance, if RPi.GPIO was used and not cleaned up, it might hold a pin).
  - Use an LED or oscilloscope to verify the PWM output if possible.

- **System Crash or Freeze:** High CPU usage (from vision processing) can cause the Pi to throttle or even freeze if it overheats. Monitor the CPU temp (`vcgencmd measure_temp`). The Limelight camera itself offloads processing, but if we do OpenCV tasks on the Pi, ensure you aren’t processing at an unnecessarily high frame rate or resolution. We stuck to 640x480 @ 30fps which the Pi 4 can handle. Also ensure adequate cooling (heatsinks or a small fan if running for extended periods in warm environments).

- **Logs and Debugging:** Always check `run.log` (generated by `logging.FileHandler` in `main_run.py`) after a test run. It will contain timestamped logs of what happened (especially if `DEBUG_MODE=True` in config, you’ll see a lot of detail). This can help identify where things went wrong (e.g., if a turn was detected or not, distances measured, etc.). We often added extra `print()` or `logging.info()` lines during development to trace execution – you can do the same and then remove or disable them (or keep them under DEBUG mode).

By following these troubleshooting tips, you can resolve most integration problems. Our Engineering Journal (below) also describes how we overcame specific challenges during development.

## Limitations and Planned Improvements

While our autonomous car is functional, there are several limitations to acknowledge and areas ripe for future improvement:

- **Simplistic Wall-Following Control:** The current wall-following uses a basic threshold and fixed steering adjustment. It works, but it’s not as smooth as it could be. In future, implementing a PID controller using the error (difference between current distance and target distance) would likely result in smoother and more stable driving, especially at higher speeds. Tuning the PID could allow faster speeds without oscillation.

- **Turn Detection Reliability:** We are relying on a single mechanism to detect turns (color sensor or camera color detection). If that sensor fails to read (e.g., in different lighting or if the marker is faint), the robot might miss a turn. One improvement is to incorporate additional cues: for example, monitor the distance sensor – if the left distance suddenly increases drastically, it could indicate the left wall ended (left turn opening). Our current code partly does this (if `dist == -1` we go straight, assuming maybe a turn), but a more robust approach could cross-verify a color signal with distance data or even use odometry (track how far we’ve traveled since last turn to predict when next turn is near, based on known course layout).

- **Obstacle Avoidance Not Fully Integrated:** The logic to avoid obstacles (pillars) using the camera was developed and tested, but due to time constraints it was not deeply integrated into the main driving loop. Currently, if an obstacle is detected, the code can steer around it, but we did not implement logic to navigate back to the center of the lane after avoiding or to handle multiple obstacles in sequence. A planned improvement is to use the camera’s data to adjust the path more intelligently – for example, detecting an obstacle at a distance and gradually curving around it, rather than a last-second swerve. Additionally, using the Limelight’s ability to detect AprilTags could be a more reliable method if the obstacles were marked with fiducials (if allowed by competition rules).

- **Parking Precision:** Our parallel parking approach is simplistic – it drives until it sees the zone and then goes forward a bit. It doesn’t ensure the robot is perfectly aligned or centered in the spot; it just tries to get fully in. In the future, we’d like to implement a proper parallel parking maneuver (perhaps a reverse-in motion if required, depending on rules). Also, using computer vision to align parallel to the parking space (checking the angle of markers or walls) could make the parking more consistent.

- **Speed vs Accuracy Trade-off:** We found that increasing speed makes everything harder – sensor readings update less frequently relative to distance covered, and momentum can cause overshooting turns. Our current maximum safe speed was determined empirically. In future, adding wheel encoders or an IMU could allow for odometry-based braking before turns or smoother deceleration. We could also implement dynamic speed control: e.g., slow down when approaching a turn or when an obstacle is detected, and speed up on straightaways. Right now, speeds are mostly constant (except for parking phase which is slow).

- **Mechanical Limitations:** The car chassis has some play in the steering and drivetrain (especially when we had the servo, there was slop around the center). The Build HAT motor for steering improved torque but still had a bit of backlash in gears. This can cause the heading to drift. A more rigid steering mechanism or feedback from an encoder could improve accuracy. We also considered adding a gyro sensor to correct heading after turns (i.e., turn 90° accurately). This was not implemented but is a logical next step for precision.

- **Use of Advanced Sensors:** The Limelight 3A is powerful – it can do vision processing on-board (like AprilTag detection at high framerates). We did not fully utilize this capability due to the learning curve and integration time. Future teams could configure the Limelight to detect specific colored targets or AprilTags and send results to the Pi (e.g., via NetworkTables or a direct network API). This would offload the vision processing from the Pi and potentially be more reliable. Additionally, integrating an inertial measurement unit (IMU) for detecting turns or collisions, and wheel encoders for distance traveled, would make the system more robust. Our design kept things relatively simple to match the competition scope, but there is room to add these.

- **Software Structure Improvements:** The code could be refactored to be more modular/flexible. For instance, the current `main_run.py` script is somewhat monolithic for the main mode. Breaking it into smaller state-machine or behavior functions could help testing and reusability. Also, better error handling (e.g., recovering from a sensor failure mid-run) could be implemented. We also thought about a “calibration mode” where the robot could calibrate its straight drive or sensor readings at start (not implemented, but could be useful if sensors vary each time).

- **Testing in Different Environments:** We tuned the robot on a particular test track. In different venues (different lighting, floor color, wall material), performance can vary. We noted that the distance sensors can behave differently on very reflective surfaces or very dark surfaces. The color sensor or camera thresholds might need adjustments for lighting. A more adaptive approach (auto-calibration or using relative contrast instead of absolute thresholds) would improve portability. This is something to consider for future iterations, especially if the competition allows a calibration period on the actual field.

- **Documentation and Team Handover:** We documented the project thoroughly (as you can see!). One limitation often is the ability for new team members to pick up where we left off. We wrote the Engineering Journal below to help with that. In the future, maintaining an updated wiki or adding more in-line code comments during development could help newcomers understand the code faster. We tried to strike a balance by writing meaningful log messages and keeping function names self-explanatory.

Despite these limitations, the project achieved its primary goals. The planned improvements listed are opportunities for the next development cycle or future teams to enhance the car’s performance and reliability. We hope this documentation and our code provide a strong foundation for those improvements.

---

# Engineering Journal (Development Log)

*Authors: Tair Kaldybayev, Ulan Gauan – WRO 2025 Future Engineers Team*

This engineering journal is a chronological account of our team’s journey developing the autonomous car. It details our initial plans, the design and building process, integration of hardware and sensors, coding and algorithm development, testing, and the challenges we faced (and solved) along the way. We write this both as a reflection on our learning process and as a guide for future team members or judges to understand how our project evolved.

## Initial Goals and Concept (Week 1)

At the outset, our goal was clear: build a self-driving model car that can complete the WRO Future Engineers 2025 challenge course. The course, as we understood from rules, would include straight sections and turns delineated by walls or lines, with random obstacles (colored pillars) placed on the track, and a final parking area that the car must navigate into. We wanted our robot to be able to:
- Follow the path (stay on track, likely hugging one side as a reference – we chose left wall following as our strategy).
- Detect an upcoming turn (left or right) reliably and make the turn.
- Recognize obstacles on the road and circumvent them without crashing or leaving the track.
- Park in the designated zone at the end of the run (parallel parking between markers).

**Design Concept:** We envisioned a car-like robot (four wheels, front-wheel steering, rear-wheel drive) to mimic how real vehicles steer, because the challenge specifically mentioned “differential drive is different from car steering” as something to learn. Using a single steering axis would also allow more precise control in tight turns (versus a differential skid-steer which could be jerky in a car scenario). We sketched a basic design:
- A chassis roughly the size of an A4 paper, with ~15cm width (to comfortably fit in lanes).
- Two large wheels at the back for drive, possibly powered by a single DC motor through a shared axle or gear train.
- Two wheels at the front for steering, connected by a tie rod so they turn together, driven by a small servo or motor.
- Mount for a Raspberry Pi and sensors on top.
- A forward-facing camera at the front (for obstacle and parking zone detection).
- Side-facing or angled sensors to measure distance to walls (for wall following).
- Swappable components (we knew we might try both LEGO components and generic parts, so we wanted a design that could accommodate either a LEGO motor or a generic motor, etc., with minimal rework).

We also decided early on to use the Raspberry Pi as the brain due to its familiarity and the need for camera processing. The Raspberry Pi 4B was available to us, and we knew it could run Python and OpenCV, which we planned to use for vision. The Pi also could interface with various sensors.

**Initial Parts Selection:** In the first week, we gathered parts we thought we’d use:
- A Raspberry Pi 4B and an SD card with Raspbian.
- Two VL53L0X Time-of-Flight distance sensors (tiny breakout boards) for measuring distance to walls on left and right.
- An HC-SR04 ultrasonic sensor (we had this as a backup for distance sensing, though ultimately we didn’t use it because the VL53L0X has better compactness and don’t require wide pulses).
- A hobby servo (TowerPro MG996R) for steering – it’s a common, strong servo with ~10kg/cm torque, enough to turn our light front wheels.
- A DC motor with gear housing (and built-in encoder, though we didn’t use the encoder initially) to drive the rear wheels. We considered a 12V DC motor from a drill or a smaller 6V DC motor from a Tamiya gearbox. We ended up with a 6V 150RPM geared motor for testing.
- L298N dual H-bridge motor driver to control the DC motor (and it could control two motors if needed, or a motor + servo (with servo on direct PWM)).
- A 7.4V 2S Li-Po battery (from an RC plane) to power the motor driver, and a 5V UBEC to power the Pi (to ensure stable voltage).
- The Limelight 3A camera – this was a bit of a wildcard. One team member had access to it, and we thought it would be great for vision (it’s essentially a Raspberry Pi Camera with a Jetson-like co-processor, designed for FIRST Robotics). We weren’t 100% sure we could integrate it with our own code, but we wanted to try because it offers high framerates and built-in vision tracking capabilities.
- We also had a LEGO Mindstorms / SPIKE Prime kit at our disposal. This included some motors and sensors. Initially, we were not planning to use LEGO parts, but we kept it in mind as a backup (especially the sensors, since the SPIKE Prime distance sensor could replace the VL53L0X if we had issues, and a color sensor could be useful).
- For turn detection, we considered using a down-facing color sensor to read colored tape on the floor or small colored cards on the track. We had an EV3 Color Sensor and a SPIKE color sensor. We tabled this decision until we had the track info. Later we learned about the red/green “road signs” in WRO rules, which could be read either by a color sensor or the camera.

By the end of Week 1, we had a rough plan and all the parts laid out. The next step was to build a prototype chassis to mount everything.

## Building the Robot Base (Week 2)

In the second week, we focused on constructing the robot’s base and integrating the major hardware components.

**Chassis Construction:** We started with an off-the-shelf small RC car frame that one member had. It had the four wheels and a simple steering mechanism (the kind where a small servo turns a rack-and-pinion or a lever to steer the front wheels). We removed the RC electronics, keeping the mechanical parts. This gave us:
- A compartment where we could fit the Raspberry Pi.
- Mounting positions for sensors (we attached a small bracket for the distance sensors on the left and right sides of the car, near the front to get an unobstructed view of the walls).
- A place at the front center to mount the camera (the Limelight).
- The steering linkages connected to a spot where originally an RC servo sat. We placed our MG996R servo there.
- A spot at the rear for a motor. The RC car had a space for a motor to drive the rear differential. We had to adapt our motor to it. We 3D-printed a coupling to connect our DC motor shaft to the driveshaft of the car. It was a bit flimsy but worked for light testing (we knew high torque might break it, but we planned to run at moderate speeds).
- We also printed a custom mount to hold the VL53L0X sensors at a fixed angle pointing slightly outward (to detect walls a bit ahead of the car, not just directly sideways). We used double-sided tape to stick these to the chassis.

**Electronics Integration:** We placed the Raspberry Pi on the chassis (using standoffs and zip ties). The L298N motor driver board was mounted toward the back (for short wires to the drive motor). The servo was powered from the L298N’s 5V regulator initially, and the Pi was powered from a USB power bank in early tests (to isolate power issues).

Wiring done in this phase:
- Servo to Pi’s GPIO 13 (for PWM), power to Pi’s 5V and ground.
- Motor to L298N outputs, L298N inputs to GPIOs (we chose GPIO 5 and 6 for IN1, IN2, and GPIO 12 for the PWM enable pin).
- VL53L0X sensors: one connected to I2C pins (SDA, SCL on GPIO 2,3). The second we connected to the alt I2C on GPIO 0,1. We soldered a wire to each sensor’s XSHUT pin as well, just in case we needed to do a software address change (this pin can disable the sensor). We connected those XSHUT wires to two spare GPIOs (GPIO 17 and 27, which were convenient).
- Limelight camera: just USB cable to the Pi. We also connected an Ethernet cable from the Limelight to a laptop at one point for configuration, but that was separate from the robot’s main wiring.

Once everything was wired, we powered it up. Immediately, we hit our first set of challenges:
- The Raspberry Pi booted, but the servo started twitching uncontrollably as soon as power was applied. This was likely due to the servo seeing some random signal during boot or the 5V line ramp-up. It scared us because the wheels would jerk fully left/right randomly. We resolved this later by not powering the servo until the Pi was up (using a switch) and by initializing the PWM output as soon as possible in code to a neutral position.
- The Pi’s console was outputting on the serial pins (we noticed because the L298N IN pins we chose happened to be GPIO 14/15 at first – which are TX/RX!). So the motor started spinning unexpectedly on boot as well. We quickly realized our mistake and re-routed those control wires to different GPIOs, leaving TX/RX for potential Build HAT use. We also disabled serial console promptly to avoid any similar issues.
- Both VL53L0X sensors were connected, but our initial I2C scan (`i2cdetect`) only showed one device at 0x29 on bus 1 and nothing on bus 0. We suspected the bus 0 wasn’t enabled or the sensor on it wasn’t powered. We discovered that the ID_SD and ID_SC pins (GPIO 0,1) by default were not configured as I2C. We edited `/boot/config.txt` to add `dtparam=i2c_vc=on` (which turns on the “video core” I2C, i2c-0). After a reboot, we saw the second sensor at address 0x29 on bus 0. Great – but both are still at 0x29 on different buses, which is fine.
- We wrote a quick Python script using the `vl53l0x` library to read distance. It worked for one sensor but not the other. It turns out the library assumed bus 1. We then decided to scrap that library and instead use SMBus directly to talk to the second sensor. This was getting complicated. At this point we considered switching to the LEGO Distance Sensors with a Build HAT to avoid these low-level issues.

**Decision Point – LEGO Build HAT Integration:** We had a Raspberry Pi Build HAT available (the new board that lets you plug in up to 4 LEGO Technic devices). Around this time, we debated: should we convert our design to use the LEGO motors and sensors? Pros:
- LEGO motors have encoders and the Build HAT library can turn them to specific angles or speeds easily.
- The LEGO distance sensor would not have the I2C address conflict issue (the Build HAT handles it via its protocol).
- We could also use a LEGO color sensor for turn detection, and maybe a LEGO motor for steering which might be more precise than our servo (which was giving us jitters).
- It could simplify our code because buildhat library is higher level (no need to manage PWM or I2C details).
Cons:
- Our mechanical chassis was not designed for LEGO parts, but we could adapt with some mounting brackets.
- The Build HAT would cover the Pi’s GPIO, making it harder to connect non-LEGO parts (like the Limelight or other breakout sensors). We realized though we could connect the Limelight via USB regardless.
- The Build HAT itself needed an 8V power input; we could use our battery for that, that was fine.
- We were somewhat late in timeline to drastically change hardware.

At this point (toward end of Week 2), we decided to partially integrate the Build HAT:
- We removed the L298N and servo connections from the Pi and instead put the Build HAT on the Pi.
- We connected one LEGO medium motor to port A (directly driving one of the rear wheels – we actually coupled it to the left rear wheel and let the differential/gearing in the RC chassis handle driving both wheels).
- Another medium angular motor to port B for steering. We built a small adapter to link the motor’s axle to the steering mechanism of the car (some LEGO beams and connectors in a makeshift way). It wasn’t a perfect fit but it held enough to turn the wheels.
- Connected a SPIKE Prime Distance Sensor to port C, mounted on the left side of the car.
- (We didn’t have a second LEGO distance sensor available immediately, so we left port D empty and kept the right VL53L0X on I2C as a placeholder for right distance. This hybrid approach was odd but we managed for testing – left sensor via Build HAT, right sensor via direct I2C.)

This hybrid was not ideal, but it allowed us to test the Build HAT motors while still reading at least one distance from the VL53. We wrote small tests to spin the motor, turn the steering motor to certain angles, etc. The Build HAT motors responded beautifully – no jitter, smooth control. That gave us confidence to fully switch to Build HAT for all critical functions. By the end of Week 2:
- Robot base physically built (with some rework to accommodate LEGO motors).
- Basic hardware integration issues identified and largely solved (especially UART conflicts, I2C config, servo jitter partially solved by replacing servo with motor).
- We were ready to dive into coding the actual autonomous behaviors.

## Sensor and System Integration (Week 3)

Week 3 was about getting all sensors and actuators working in unison and starting to develop the algorithms for navigation.

**Dual Distance Sensors Working:** We obtained a second SPIKE Prime Distance Sensor at the start of this week, so we could use the Build HAT for both left and right distances. This was a relief, as we could drop the VL53L0X and its complex setup. We mounted the second sensor on the right side of the car. Now ports A, B, C, D of Build HAT were all occupied (Drive motor, Steering motor, Left distance, Right distance). We tested reading from both sensors rapidly and it worked, though we noticed that reading them one after the other had a slight delay (the Build HAT processes one sensor at a time). That was fine.

We wrote `ultrasonic_left.py` and `ultrasonic_right.py` to wrap these sensors. We decided on averaging a few readings to smooth noise. Initially, we tried continuous mode (BuildHAT’s DistanceSensor can call a callback whenever distance changes), but that was too event-driven and complicated to integrate with our loop. Polling them at 10Hz in our main loop was sufficient.

**Turn Detection Approach:** The major question was how to detect when to turn left or right. The WRO rules indicated some kind of road signs or colored markers. After some research and Q&A from previous year (2024), we learned that typically:
- They place a **red-colored marker on the left side of the road** where a left turn is coming up.
- A **green-colored marker on the right side** where a right turn is coming.
These could be small upright signs or markings on the floor. In either case, color is the key indicator.

We had two ways to detect color:
1. Use a small color sensor (like the LEGO color sensor) pointed at the spot where the sign would appear.
2. Use the camera to detect the color of objects in front.

We chose to go with a dedicated color sensor for turn detection for simplicity and speed (camera processing could be slower and more error-prone for this, plus the camera was needed for obstacle detection primarily).

However, we had no free ports on Build HAT for a LEGO color sensor now. We considered switching the right distance sensor back to a custom sensor and freeing port D for a color sensor, but that felt like a step backward in reliability. Alternatively, use an I2C color sensor (like an Adafruit TCS34725) on the Pi’s I2C. We did have a TCS34725 from a previous project.

So we connected the TCS34725 color sensor module to the Pi’s I2C bus (since we freed it after removing VL53s). We pointed this small sensor out the front-left side of the car, where it might see a red sign, and front-right for green. Realizing one sensor can’t see both sides well, we actually mounted it angled forward, and wrote logic to differentiate red vs green. Our `sensors/color_line.py` (misnamed a bit, but essentially color detection) would read RGB from the sensor and decide:
- If it sees a strong red component -> return "left"
- If strong green -> return "right"
- Otherwise None.

We had to calibrate this by putting colored paper in front of the sensor and noting values. Under competition lighting, this might vary, so we kept thresholds a bit conservative and also included ranges from WRO (like the exact RGB values given, but since ours gives raw counts, we normalized them).

In parallel, we wrote a fallback: if the color sensor returns None but the left distance sensor suddenly returns -1 (meaning wall disappeared on left), that could indicate a left turn if we haven’t taken one recently. This was a heuristic we thought of as backup.

**Obstacle Detection with Camera:** With turning and wall-following sensors in place, we turned attention to obstacle detection. We knew obstacles are colored pillars (likely the red and green ones used as “road signs” might double as obstacles placed on the track). The rules said road signs must be obeyed on the laps, but after the last lap on the way to parking, obstacles could be passed on either side freely. So our plan:
- During the laps, if an obstacle is in the way, ideally we go around the correct side (left side for a pillar that indicates something? But rules said on last segment you can pass on either side).
- It got a bit confusing, so we simplified: if obstacle (pillar) detected, we’ll choose a side to go around it based on which side of the lane is clear.

We used the Limelight camera for this. We spent a good amount of time getting familiar with the Limelight’s interface:
  - We connected to `limelight.local:5801` in a browser and saw the camera feed. 
  - We tried the built-in thresholding: The Limelight can be set to detect retro-reflective tape normally (for FRC), but we configured a pipeline for plain color detection. We set one pipeline to detect red objects and another for green, just to see if we could use it directly. The Limelight was showing contours and target offsets (tx, ty values) for the largest blob of the target color.
  - Our initial idea was to let the Limelight do all the work and then query it for the results (it can output data via NetworkTables). However, integrating NetworkTables on the Pi in Python (using `pynetworktables`) was an additional complexity, and since we already had OpenCV in our project, we decided to just do custom vision in Python reading the frames.
  - We did use the Limelight interface to fine-tune camera settings (increased exposure a bit to detect the bright colors, turned off any LED as we didn’t need illumination, and set resolution to 640x480 at 90fps for a good balance of FOV and speed).

Coding the obstacle detection:
- We capture a frame (640x480).
- Convert to HSV, blur a bit.
- Create masks for red and green. For red, we had to combine two ranges (hue around 0 and around 180). We ended up with something like HSV in [0±10, sat>100, val>100] and [170 to 180, sat>100, val>100] combined.
- For green, hue ~ 50-85 (as per typical green).
- We used `cv2.findContours` on the masks. For each contour found, we bound them with `cv2.boundingRect` and determined if it’s on left half or right half of the image (by comparing the x coordinate of the center to image width/2).
- We labeled each detection as "red-left", "red-right", "green-left", "green-right" for debugging.
- Our decision logic (`analyze_obstacle`) was: if any pillar is detected:
   - If a green pillar is detected and it’s on the right side, that likely means a right turn sign (so not exactly an obstacle to avoid, it’s a sign). But if it’s literally on the road, maybe it *is* the obstacle. We realized the sign and obstacle might be physically the same object or different – the game description wasn’t crystal clear to us. We assumed obstacles could be anywhere, not necessarily at turn markers.
   - Ultimately, we decided: if any pillar detected roughly in front (center of image), we need to avoid. We would choose to avoid on the side that is opposite to where the pillar is seen. So if we see a pillar slightly to left of center, we go right, and vice versa.
   - So we set `direction = "left"` if an obstacle is more to the right half (meaning go left around it), and `direction = "right"` if obstacle is on left half.
   - If both red and green were seen (unlikely at same time), we might prioritize one – but we didn't fully implement multi-obstacle scenarios.

We tested this by placing a red cone in front of the robot and seeing if it outputs left or right. It was a bit finicky but worked in a controlled scenario.

**Driving and Steering Tuning:** We now integrated the driving logic with sensor input. We wrote a draft of `main_run.py` that:
- Continuously drives forward at a moderate speed.
- Checks `check_turn_color()` each loop; if it returns something, do the turn maneuver.
- Otherwise, adjust steering slightly based on left distance as described earlier (this was easy to implement).
- We also put a condition: if the color sensor hasn’t triggered a turn and we see left distance go to -1 for a short while, assume it’s a left turn and execute it anyway as a fallback (in case the color sensor missed it).
- For right turns, since we hug left wall, a right turn would manifest as the left wall suddenly receding (distance increasing a lot). That plus maybe seeing a green marker would cue a right turn. We handled that similarly.

We tuned `TARGET_DISTANCE_MM` to about 300 mm (30 cm) because the track width seemed around 50-60 cm, so being 30 cm from left wall is a good middle. We set tolerance ±10 mm for adjustments.

We tested the car on a simple oval track we made with cardboard walls. Left turns were working via color sensor triggers (we manually put a red paper when we wanted it to turn left). The car would see red, log "left turn", call our `turn_left()` which at that time simply:
  - Steered full left (25°),
  - Drove forward for 0.5 seconds,
  - Straightened wheels.
This actually turned the car ~90 degrees surprisingly well, given the moderate speed and wheel traction.

Right turns (with green) we tested less (our test track was mostly left turns as per WRO field might be, with one right turn in the end). But they were analogous.

**Issue – Oversteering and Oscillation:** As we increased the speed to test how fast we could go, we noticed that the wall following started oscillating: the robot would drift a bit from wall, correct inward, then too close, correct outward, etc., sometimes even leading to a slight S-shape motion. This is where we realized a proper control loop was needed. We attempted a quick fix: reduce the correction angle from 5° to 3° and increase the correction frequency. This helped a bit but not perfect. We left this as "good enough for now", thinking we might revisit if time permits (which it eventually didn’t extensively).

We also observed occasional big swings when a turn was detected late – one time the car almost missed a left turn because the detection was slightly delayed and it turned very sharply to catch it, almost hitting the far wall. After that, we decided to proactively slow down when approaching where a turn might be. We did this by using the turn counter: if we know 4 turns per lap, as the count gets to 3, we anticipate the 4th and maybe reduce speed slightly. This was a heuristic; not very exact, but we tried a small speed reduction in code before an expected turn. (In practice, not a huge effect, but conceptually future could incorporate map knowledge).

By end of Week 3:
- The integrated system could complete a simple test track with one lap and a dummy parking zone.
- We had not implemented the actual parking logic yet, just a placeholder to stop at some point.
- The obstacle avoidance was coded but not tested on a real random obstacle insertion (we needed a scenario to test that).
- We started logging data to fine-tune – e.g., printing distance every loop to see variation, printing when turns detected, etc. These logs were helpful to adjust parameters.

## Testing, Tuning, and Issues Encountered (Week 4)

Week 4 was intense testing and debugging, as well as implementing the parking maneuver and final touches. We also encountered some unexpected issues.

**Parallel Parking Implementation:** The WRO challenge requires the robot to park between two markers at the end. Based on known rules, the parking area is on the left side after the last turn (for 2024, it was like after finishing laps, you turn left into a parking bay). We assumed something similar: after the final lap’s last turn, there will be a parking zone on the left with two markers forming the “entrance” of the parking spot.

We decided to use the camera to identify the parking zone markers. If they were like two green pillars or some AprilTags, it would be easier, but we weren’t sure. We assumed maybe two distinct colored objects or simply an open area that the camera could distinguish (the floor color of parking zone could differ?).

Our approach in code:
- After completing all laps (lap_counter == TOTAL_LAPS), we start looking for a parking indicator.
- We slow the car down (PARKING_SPEED ~30) and move forward slowly, capturing frames.
- We wrote `detect_parking_zone()` to look for a large gray or black area or perhaps a pair of lines. Actually, given lack of exact info, our placeholder was to reuse the color sensor or camera to find something unique. In our test, we placed two black tape strips as markers and programmed detect_parking_zone to simply look for a significant dark region in the bottom of the frame.
- Once found, we stop and then move a tiny bit further to ensure fully inside the zone, then stop completely and declare success.

We tested a scenario: a “parking” area marked by two pieces of paper on floor. The detection was very naive, but it did succeed in our controlled test (we set it to detect a sudden increase in green color, as if the parking area had green tape).

**Challenges During Testing:**

We ran the robot through many trial runs and faced these issues:

- **Inconsistent Color Sensor Reads:** Our TCS34725 color sensor sometimes gave fluctuating readings under different light. At times, it would falsely think it saw a bit of red when none was there, due to sunlight or shadows. This caused an occasional false trigger of turn when not intended. To mitigate, we added a requirement that the color must be consistently seen for a few loops (like 3 readings in a row) before we accept it as a turn signal. We also shielded the sensor with a little paper hood to prevent overhead light interference.

- **Camera Frame Rate Drop:** At one point, the camera processing thread (when we visualized on screen using `test_obstacle_camera.py`) was slow (~5-10 FPS). We realized we had accidentally left the resolution at 960x720 in one test, which was too high. Dropping back to 640x480 and ensuring we weren’t doing any heavy drawing unless needed fixed this. In actual runs, we don’t display the image, we just process it, which is faster.

- **Power Problems:** During longer runs, our battery voltage dropped and the Build HAT’s LED went red, meaning motor power was low. This caused the motors to run slower and sometimes the steering motor would not center properly. We then made sure to charge batteries fully and also carry spares. We also added a check in code to log the input voltage (BuildHAT library can get input voltage). If it fell below ~7V, we’d know we were in trouble. In future, a DC-DC converter from a higher battery could stabilize this.

- **Build HAT Serial Bug:** We encountered a strange bug: occasionally on starting the program, the Build HAT library would throw an error like “Serial port busy” or simply never return from Motor initialization. This was rare but happened twice. We discovered it might be because a previous run wasn’t closed properly and the serial port was stuck. A reboot fixed it. We then always ensured to stop the program with KeyboardInterrupt (which triggers our cleanup to stop motors and presumably close the port). Additionally, we learned you can call `hat = BuildHAT()` and `hat.close()` (though our use of the library was mostly implicit). We just kept an eye on this. In a competition scenario, a power cycle of the Pi would also reset it.

- **Integration of Obstacle Avoidance:** We tried a full run with an obstacle. The car approached, our `analyze_obstacle()` flagged “go left”. We had not yet coded automatic action for this in `main_run.py` (because we were cautious not to conflict with turn logic). So in this test we manually intervened (basically picked up the robot and placed it as if it went around). This obviously is not a solution – so we carved out time to integrate it properly:
  - We decided to integrate obstacle avoidance only when not near a turn. If a turn is imminent (say we detected color or wall drop), that takes precedence.
  - Otherwise, if obstacle detected, we execute a quick avoid: steer and perhaps also adjust motor.
  - We ended up implementing it in the `speed_run` loop more clearly (because speed run is continuous, obstacle avoid can fit in). In `main_run`, due to the complexity, we put it in test mode and left it out of final main run because we weren’t fully confident it wouldn’t misfire on a legitimate road sign. Essentially we consciously left a gap in full autonomy: we hoped obstacles would not be placed in such a way to completely block us at turns. If they did, maybe our manual driving or backup would come into play. (If this were a real competition, that’s a risk; ideally we’d finalize this but time pressed.)

- **Oversteer at final turn to parking:** In one test, after finishing laps, the car overshot the entrance to the parking zone (it turned a bit wide). This made it miss detecting the parking zone until it was partially past it. To solve this, we made the car slow down on the very last turn and also ensured the camera was definitely on for parking search. We also added a slight right steering bias if it’s going into the parking (to hug the wall as it turns in). This somewhat improved the positioning.

- **Software Reinstallation:** At one point, the Pi started having odd behaviors (couldn’t import OpenCV after an update, and BuildHAT library threw Python errors which looked like version mismatches). We realized the Python environment got messed up (maybe by mixing apt-get install and pip for OpenCV, causing conflicts). Given the time, we decided to wipe and do a fresh install of Raspberry Pi OS, then only use pip for everything. This cost us half a day but cleared many random issues. We documented the exact steps (which became part of the installation instructions above). After reinstall, everything was consistent.

By the end of Week 4, the robot could:
- Start driving, complete 3 laps of our test track, and initiate a parking sequence.
- It correctly responded to our simulated turn signals (colored markers we placed).
- It could avoid a test obstacle in speed_run mode, though we were a bit uneasy about obstacle avoidance in the main run due to aforementioned reasons.
- Most importantly, we were learning a ton about what worked and what didn’t, which we noted for future improvements.

## Final Adjustments and Last-Minute Rebuild (Week 5 - Competition Week)

As the competition drew near (week 5), we had to finalize everything. However, we made a bold decision: **rebuild the robot base and clean up the code one more time**.

We realized some mechanical issues (loose steering linkage, mediocre motor coupling) could jeopardize us. Also, our code had accumulated some test logic and hybrid approaches that we weren’t using. So, in the last days:
- We rebuilt the chassis using more LEGO components: we actually switched to using a LEGO frame for the front steering entirely. We attached LEGO wheels (smaller, but nicely fit on the Technic hubs) and a LEGO steering mechanism from an old Technic set onto our base. This reduced slop significantly. The back wheels we kept the larger ones but mounted them directly on a LEGO axle driven by a LEGO large motor. Yes – we ended up going almost full LEGO for drivetrain: Large motor (port A) driving rear axle, Medium angular motor (port B) for steering front axle.
- The distance sensors remained on left and right but we fixed their mounting better (hot glue onto the frame at consistent angles).
- The Limelight camera was firmly mounted at front-center and we added a slight downward tilt to it so that it could see closer obstacles and the ground markers (previously it was horizontal).
- We adjusted weight distribution – the battery pack was moved center to not tip the car on turns.

This hardware rebuild improved our test runs’ consistency a lot. The car now turned more predictably and didn’t wobble as much (LEGO components added some weight but also stability).

On the software side, we performed a “code freeze” 2 days before competition:
- Removed or commented out any debug GUI stuff (to avoid accidental window pop-ups).
- Ensured all print statements were either necessary or converted to logging.
- Verified the mode system works by testing each mode one by one.
- Updated README (which you are reading) and created this EngineeringJournal, as part of the deliverables and also to solidify our understanding.
- Each team member took turns operating the robot to make sure the instructions were clear and everything could be started easily (so that in competition any of us could set it up if needed).

**Collaboration and Teamwork:** Throughout the project, teamwork was crucial. Tair and Ulan shared responsibilities fluidly. For example, when one was focusing on coding the steering logic, the other would be adjusting the hardware alignment of the wheels. When debugging sensors, one person would monitor logs and code, while the other carefully moved the robot or placed obstacles to see responses. We often brainstormed together on whiteboard for logic (like how to combine sensor triggers for turn decisions). This collaborative approach helped us catch each other’s mistakes – e.g., Tair wrote an early version of the `speed_run` logic, and Ulan noticed that if both walls disappeared (an open area), the code didn’t handle it; we then added a condition for that. Similarly, Ulan mounted the distance sensors initially a bit too high; Tair suggested angling them down to better catch low walls – a small but effective change.

We also split tasks occasionally: Ulan took lead on the vision processing part (getting the Limelight working, writing OpenCV detection code), since he had prior experience with OpenCV. Tair concentrated on the movement control and integration (ensuring the Build HAT motors did what they should, writing the main loop structure). We would then integrate these parts together, testing as a team.

Communication was also key. We held short daily sync meetings discussing what was done and what’s next. We used a shared Google Doc to jot down bugs encountered during testing and tick them off when solved. This helped ensure by the end we didn’t forget any known issue unaddressed.

Finally, on the last day before the competition, we did a full end-to-end run in a makeshift course that resembled the expected official one as closely as possible. The robot performed decently – it completed laps, avoided an obstacle we placed (though somewhat widely), and parked with a slight misalignment but within bounds. This was a big moment for us, seeing all the pieces come together.

We packed up the robot, ensuring all wiring was secure, and printed out this documentation for reference. Nervous but excited, we headed into the competition knowing that regardless of the outcome, we had built something complex that works and learned invaluable lessons in the process.

## Conclusion

The development of the WRO2025 autonomous car was a challenging yet rewarding journey. We started with ambitious ideas and faced numerous hurdles, from hardware conflicts to algorithmic puzzles. Through iterative design, testing, and teamwork, we built a robot that meets the core objectives of the challenge. Not everything was perfect – there are many ways the system can be improved as we’ve detailed – but given the time and resources, we’re proud of what we accomplished.

This engineering log captures the evolution of our thought process and the rationale behind changes. For future teams or new members, our advice would be:
- Don’t be afraid to change course if something isn’t working (like how we switched hardware mid-way to leverage LEGO components).
- Test often and in conditions as close to real as possible – every iteration taught us something new.
- Work together and use each other’s strengths. Robotics is inherently interdisciplinary; having multiple viewpoints helps.
- Document as you go. We sometimes were so deep in fixing things we forgot to log it. Writing this after the fact was possible because we had a lot of commit messages, code comments, and some notes, but it’s best to jot down key decisions in real-time.

We hope this documentation and our codebase will be useful for anyone looking to understand or build upon our project. Maybe it will even inspire future participants to push the boundaries of what these small autonomous cars can do. Good luck to future teams, and happy building!

***End of Engineering Journal***
