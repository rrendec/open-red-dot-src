import time
import gpiod
from gpiod.line import Direction, Value

CHIP_PATH = "/dev/gpiochip2"
OFFSETS = list(range(8))

# Step 1: Initialize all 8 lines as inputs
init_config = {
    offset: gpiod.LineSettings(direction=Direction.INPUT)
    for offset in OFFSETS
}
req = gpiod.request_lines(CHIP_PATH, consumer="pcf8574_test", config=init_config)
print("Initialized all lines as inputs.")
req.release()

# Step 2: Sequentially set line to output (0), wait 500 ms, then revert to input
for offset in OFFSETS:
    print(f"Line {offset}: Setting to OUTPUT (0)")
    out_config = {
        offset: gpiod.LineSettings(
            direction=Direction.OUTPUT,
            output_value=Value.INACTIVE # Logical 0
        )
    }
    req = gpiod.request_lines(CHIP_PATH, consumer="pcf8574_test", config=out_config)
    time.sleep(0.5)
    req.release()

    print(f"Line {offset}: Reverting to INPUT")
    in_config = {
        offset: gpiod.LineSettings(direction=Direction.INPUT)
    }
    req = gpiod.request_lines(CHIP_PATH, consumer="pcf8574_test", config=in_config)
    req.release()

print("Sequence complete. All lines released.")
