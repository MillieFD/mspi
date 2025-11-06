"""
This example script demonstrates how to use the Thormotion library. Requires a connected Thorlabs motorized XY stage.
See https://software.zaber.com/motion-library/ for more information.

The program:
    1. Establishes connection with the stage
    2. Homes both axes if needed
    3. Executes the raster scan pattern
    4. Handles alerts and disconnection events

Raises:
    ValueError: If no Zaber devices are detected
"""

import asyncio

from thormotion import KDC101

# PARAMETERS: The system will scan a square area defined by two corners (start & end)

# Define the starting coordinates
x_start = 0 # mm
y_start = 0 # mm

# Define the end coordinates
x_end = 10 # mm
y_end = 10 # mm

# Define the step size between adjacent points (resolution)
step = 0.100 # mm

# SETUP

# Find the Thorlabs devices
x = KDC101("ENTER SERIAL NUMBER HERE")
y = KDC101("ENTER SERIAL NUMBER HERE")

# Open USB communication
x.open()
y.open()

# Home axes if needed
if not x.is_homed():
    x.home()
if not y.is_homed():
    y.home()

# RASTER: Move in a raster scan pattern

# Move to the starting position
x.move_absolute(x_start)
y.move_absolute(y_start)

while x.get_position() <= x_end:

    # Move the y-axis from START to END coordinates
    while y.get_position() <= y_end:
        # Move the y-axis to the specified position
        y.move_relative(step)

    # Reset y-axis to start coordinate
    y.move_absolute(y_start)

    # Increment x-axis to scan the next row
    x.move_relative(step)

# SHUTDOWN: Return motors to origin

async def reset():
    # Create a coroutine that returns both axes to 0 mm simultaneously
    await asyncio.gather(x.move_absolute_async(0), y.move_absolute_async(0))

# Run the coroutine and wait for all tasks to complete
asyncio.run(reset())

# End of program
print("Raster scan complete")
