# Development Tools

These tools have been used during the development of the Open Red Dot firmware.
They are not directly included in the firmware.

## Matrix Scanning

The laptop keyboard has a ribbon cable that is connected directly to the
keyboard matrix. The ribbon has 36 wires, and the web references I could find
claim that the matrix size is 16x8, so 24 wires. Some of the other 12 wires are
likely used for the key LEDs (Esc, F1, F4, Caps Lock).

Manually identifying the connections is a tedious job. It's much easier to
connect all 36 wires to some GPIO lines and continuously scan all possible
combinations in software, while pressing the keys one by one.

Raspberry Pi is an attractive platform because it runs Linux and the prototype
code can run directly on top. It is also very easy to develop/test the code
there because it can be modified in-place. However, the board does not have
enough GPIO lines.

The PCF8574 I/O expander is a very good fit for the matrix scanning job due to
its quasi-bidirectional design:
* All pins are open-drain type when used as outputs.
* A single register controls both the output value and the direction:
  * A bit value of 1 (power-on default) pulls the pin HIGH through a weak 100 uA
    current source. In this mode, the pin can act both as a weak HIGH output or
    as an input (because the weak internal pull-up can be safely overridden by a
    stronger external pull-down).
  * A bit value of 0 pulls the pin LOW through a strong internal current drain.
    In this mode the pin acts as a strong LOW output.
  * Reading the register provides the current level (LOW/HIGH) of all pins.

The PCF8574 can be connected directly to the keyboard matrix without requiring
any additional parts.
* By default, all pins are HIGH, acting as inputs.
* One pin at a time is set to output/LOW.
* When a key is pressed, if it's connected to the LOW pin on one line, it will
  pull low the other line, which is connected to another pin. That pin will also
  be pulled LOW (through the pressed key and the output/LOW pin).
* The host already knows which pin is pulled LOW through configuration. By
  scanning all the other pins and checking which one is also LOW, it can find
  what two lines the key is connected to.

Conveniently, the weak 100uA current source makes the configuration safe for the
keyboard LEDs too, e.g. when the pin connected to the cathode is configured as
output/LOW and the one connected to the anode is configured as input/HIGH.

Because the ribbon has 36 wires and a PC8574 has only 8 pins, 5 different chips
are needed to connect all the wires. The lower 3 bits of the I2C address can be
configured by external pin strapping, which allows directly connecting up to 8
chips to the same bus.

### GPIO Test Code

The `gpio-test` subdirectory contains sample code for three different methods of
driving the PCF8574 connected to a Raspberry Pi. See the corresponding
[README.md](gpio-test/README.md) file for details.

The method of choice is to drive the PCF8574 by using the generic I2C API in
Linux/Python and directly access the PCF8574 register. For matrix scanning:
* Setting a new pin as output/LOW and setting back the previous pin as
  input/HIGH can be done in a single write (if both pins are on the same PCF8574
  chip, of course).
* A single read gets the level of all 8 pins. This makes it very easy to detect
  the "other" LOW pin by doing only 5 reads (one per chip).
