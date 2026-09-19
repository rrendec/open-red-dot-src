import time
from smbus2 import SMBus

# I2C Bus 1, Address 0x20
I2C_BUS = 1
I2C_ADDR = 0x20

# In PCF8574: 1 = Input / High, 0 = Output Low
ALL_INPUTS = 0xFF

def main():
    with SMBus(I2C_BUS) as bus:
        try:
            # Step 1: Initialize all 8 lines as inputs
            print("Configuring all 8 lines as INPUTS (0xFF)...")
            bus.write_byte(I2C_ADDR, ALL_INPUTS)

            # Step 2: Sequentially set each pin to Output 0 for 500 ms, then revert to Input
            for bit in range(8):
                # Mask with 0 at current bit position, 1 everywhere else
                mask = ~(1 << bit) & 0xFF
                print(f"Pin {bit}: Setting to OUTPUT 0 (writing 0x{mask:02X})")
                bus.write_byte(I2C_ADDR, mask)

                time.sleep(0.5)

                print(f"Pin {bit}: Reverting to INPUT (writing 0xFF)")
                bus.write_byte(I2C_ADDR, ALL_INPUTS)

        finally:
            # Step 3: Release all lines back to INPUT mode on exit
            print("Releasing all lines to INPUT mode...")
            bus.write_byte(I2C_ADDR, ALL_INPUTS)

if __name__ == "__main__":
    main()
