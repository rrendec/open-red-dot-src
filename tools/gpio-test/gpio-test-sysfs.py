import os
import time

# Line base and range setup
BASE_GPIO = 504
NUM_LINES = 8
GPIO_LINES = [BASE_GPIO + i for i in range(NUM_LINES)]

SYSFS_GPIO_DIR = "/sys/class/gpio"

def export_gpio(line):
    """Export GPIO line if not already exported."""
    line_path = f"{SYSFS_GPIO_DIR}/gpio{line}"
    if not os.path.exists(line_path):
        with open(f"{SYSFS_GPIO_DIR}/export", "w") as f:
            f.write(str(line))
        # Brief pause to allow sysfs node creation
        time.sleep(0.05)

def unexport_gpio(line):
    """Unexport GPIO line."""
    line_path = f"{SYSFS_GPIO_DIR}/gpio{line}"
    if os.path.exists(line_path):
        with open(f"{SYSFS_GPIO_DIR}/unexport", "w") as f:
            f.write(str(line))

def set_direction(line, direction):
    """Set line direction ('in' or 'out')."""
    with open(f"{SYSFS_GPIO_DIR}/gpio{line}/direction", "w") as f:
        f.write(direction)

def set_value(line, value):
    """Set line output value (0 or 1)."""
    with open(f"{SYSFS_GPIO_DIR}/gpio{line}/value", "w") as f:
        f.write(str(value))

def main():
    try:
        # Step 1: Initialize all 8 lines and set to input
        print("Initializing lines 504–511 as inputs...")
        for line in GPIO_LINES:
            export_gpio(line)
            set_direction(line, "in")

        # Step 2: Sequentially pulse each line low for 500 ms
        for line in GPIO_LINES:
            print(f"Testing GPIO {line}: Setting to OUTPUT (0)")
            set_direction(line, "out")
            set_value(line, 0)

            time.sleep(0.5)  # Wait 500 ms

            print(f"Testing GPIO {line}: Reverting to INPUT")
            set_direction(line, "in")

    finally:
        # Step 6: Release (unexport) all GPIO lines before exit
        print("Cleaning up and releasing all GPIO lines...")
        for line in GPIO_LINES:
            unexport_gpio(line)

if __name__ == "__main__":
    main()
