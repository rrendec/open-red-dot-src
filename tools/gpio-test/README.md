# GPIO Test Code

Sample code for three different methods of driving a PCF8574 chip connected to a
Raspberry Pi. See the [README.md](../README.md) file in the parent directory for
the full context of how this helps.

## Pin Output Tests

All these examples assume a single PCF8574 at I2C address 0x20 and cycle through
each pin by toggling it to output/LOW and back to input/HIGH with a 0.5 seconds
delay.

The test rig includes an LED and 1K resistor connected to each pin, like so:
```
                                           3V3
    +-----------+                         -----
    |           |      LED        1K        |
    |  PCF8574  +------|<|------/\/\/\------+
    |           |
    +-----------+
```

### Device Tree Overlay

A device tree overlay is required for the first two methods, where the PCF8574
is driven by the dedicated Linux driver. Because the I2C bus is not enumerable
and discoverable, the device tree overlay is used to inform the kernel what I2C
bus the PCF8574 chips are attached to and what their addresses are.

To build the device tree overlay:
```
dtc -o pcf8574.dtbo pcf8574.dtso
```

To install the overlay, edit `/boot/firmware/config.txt` and add this line:
```
dtoverlay=pcf8574
```

### Legacy access over sysfs: `gpio-test-sysfs.py`

The Raspberry Pi OS kernel carries a patch that readds the legacy sysfs based
GPIO interface that was removed upstream.

### Modern gpiod (v2 API) access: `gpio-test-gpiod.py`

While this works (on any recent enough kernel), it has some drawbacks:
* The line is "requested" (from gpiod) for every pin state change. A lot happens
  under the hood for each of these requests.
* It's assumed that the pin state doesn't change after a requested line is
  released. This is not guaranteed by gpiod.

### Direct PCF8574 access: `gpio-test-smbus.py`

This is the simplest and most efficient access method because it eliminates any
library and kernel overhead in manipulating the GPIO lines. It is ideal for a
GPIO device as simple as the PCF8574.

On Raspberry Pi, the I2C bus is activated by default when an overlay for an I2C
device is added (as described above). However, in the absence of any such
overlay, the I2C bus must be activated explicitly by adding the line below to
`/boot/firmware/config.txt`:
```
dtparam=i2c_arm=on
```

## Pin Input Tests

### I2C Connection Test: `gpio-read-smbus.py`

Unlike the previous pin output tests, this test assumes that all five PCF8574
chips required for keyboard matrix scanning are connected to the I2C bus. It
uses the direct access method described above and prints the register value of
each of the five devices.

The main purpose of this test is to validate that all five PCF8574 chips are
connected correctly to the I2C and the address strapping pins are configured
correctly as well.
