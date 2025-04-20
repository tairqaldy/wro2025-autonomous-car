# main.py
# Autonomous car control system with mode selection

from routines.main_run import main_autonomous_run
from routines.speed_run import fast_speed_run
import sys
import time

def run_selected_mode():
    """
    Reads the mode from mode.txt and executes the corresponding routine.
    Falls back to 'main' mode if file not found or invalid mode specified.
    """
    try:
        with open("mode.txt", "r") as file:
            mode = file.read().strip().lower()
    except FileNotFoundError:
        print("⚠️ mode.txt not found, defaulting to 'main' mode")
        mode = "main"
    except Exception as e:
        print(f"⚠️ Error reading mode.txt: {e}, defaulting to 'main' mode")
        mode = "main"

    # Add a small delay to ensure all systems are ready
    time.sleep(1)

    if mode == "main":
        print("🚗 Starting main autonomous route...")
        main_autonomous_run()
    elif mode == "speed":
        print("⚡️ Starting speed run...")
        fast_speed_run()
    else:
        print(f"❗️ Unknown mode: {mode}, defaulting to 'main'")
        main_autonomous_run()

if __name__ == "__main__":
    try:
        run_selected_mode()
    except KeyboardInterrupt:
        print("\n🛑 Program stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)
