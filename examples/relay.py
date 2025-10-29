"""
This example script demonstrates how to control the Raspberry Pi 5 GPIO using the `libgpiod` library.
The mspi platform uses a Raspberry Pi 5 Relay Board that switches on/off under GPIO control.
See https://www.waveshare.com/wiki/RPi_Relay_Board for more information.

The program:
    1. Dynamically resolves BCM GPIO numbers
    2. Configures three header pins (37, 38, 40)
    3. Assigns each pin to a key (1, 2, 3)
    4. Switches on/off when key is pressed
    5. Handles keyboard interrupts and disconnection events
"""

import sys
import termios
import tty

import gpiod
from gpiod.line import Direction, Value

# SETUP: Configuring the hardware

# Adjust the hardware configuration as needed:
# 1. Resolve GPIO chip path
# 2. List keybindings for GPIO pins
# 3. Define OFF logic level (HIGH or LOW)

CHIP = "/dev/gpiochip0"
PINS = {"1": 26, "2": 20, "3": 21}  # Pins to control (BCM “Broadcom” numbering scheme)
OFF = gpiod.line.Value.ACTIVE

# Automatically determine ON value

ON = Value.ACTIVE if OFF == Value.INACTIVE else Value.INACTIVE
print(f"ON is {"HIGH" if ON == Value.ACTIVE else "LOW"}")

# Print user instructions

for k, v in PINS.items():
    print(f"Press key {k} to switch GPIO{v} ON/OFF")
print("Press any other key to exit")

# Save existing terminal settings

fd = sys.stdin.fileno()
settings = termios.tcgetattr(fd)

# CONNECT: Reqeust control of the GPIO lines

try:
    with gpiod.request_lines(
            CHIP,
            consumer="cc-relay",  # Arbitrary process name
            config={pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=OFF) for pin in PINS.values()},
    ) as request:

        # LOOP START: Main event loop repeats indefinitely until interrupted

        while True:

            # INPUT: Read characters immediately without waiting for Enter
            # 1. Enable stdin raw
            # 2. Read one character
            # 3. Restore terminal settings

            tty.setraw(fd)
            ch = sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)

            # OUTPUT

            if not ch:
                # ch is not a valid character
                raise ValueError("Encountered invalid character")
            elif ch in PINS:
                # ch is a valid key
                pin = PINS[ch]
                val = ON if request.get_value(pin) == OFF else OFF
                request.set_value(pin, val)
                print(f"Set relay {ch} (GPIO{pin}) {"ON" if val == ON else "OFF"}")
            else:
                # ch is a valid non-key character
                break

        # LOOP END: Repeats indefinitely until interrupted

except KeyboardInterrupt:
    pass
finally:
    # Disconnect: Release control of the GPIO lines
    with gpiod.request_lines(
            CHIP,
            consumer="cc-relay-shutdown",  # Arbitrary process name
            config={pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=OFF) for pin in PINS.values()},
    ) as request:
        for pin in PINS.values():
            request.set_value(pin, OFF)
        print("Released GPIO lines")

    # Restore terminal settings
    termios.tcsetattr(fd, termios.TCSADRAIN, settings)

    # End of the program
    print("Relay test complete")
