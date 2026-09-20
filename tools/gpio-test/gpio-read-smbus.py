from smbus2 import SMBus

I2C_BUS = 1
I2C_ADDR = 0x20

def main():
    with SMBus(I2C_BUS) as bus:
        for dev in range(5):
            addr = I2C_ADDR + dev
            val = bus.read_byte(addr)
            print(f"bus {I2C_BUS} addr 0x{addr:02x}: 0x{val:02x}")

if __name__ == "__main__":
    main()
