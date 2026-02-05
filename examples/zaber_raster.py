"""
This example script demonstrates how to use the Zaber Motion library. Requires a connected Zaber motorized stage with
two or more axes. See https://software.zaber.com/motion-library/ for more information.

The program:
    1. Establishes connection with the stage
    2. Homes both axes if needed
    3. Executes the raster scan pattern
    4. Handles alerts and disconnection events

Raises:
    ValueError: If no Zaber devices are detected
"""

from zaber_motion.ascii import Connection

with Connection.open_serial_port("dev/tty/USB0") as connection:
    # OPTIONAL: Subscribing to alerts

    # When the device raises an alert, Zaber Motion invokes the corresponding event.
    # 1. Create a lambda function to handle the alert
    # 2. Subscribe to the event
    # 3. Zaber Motion will execute the lambda fn each time the event occurs (e.g. to handle the alert)

    # Define a lambda fn to print alerts
    connection.alert.subscribe(lambda alert: print("Alert:", alert))

    # Define a lambda fn to raise an error if the device disconnects
    connection.disconnected.subscribe(lambda err: print("Disconnected:", err))

    # Enable alerts for all devices on the connection.
    connection.enable_alerts()

    # DETECT: Find the Zaber device

    # Search the specified connection for all Zaber devices
    device_list = connection.detect_devices()

    try:
        # One device found i.e. len(device_list) = 1 SUCCESS
        (device,) = device_list
    except ValueError:
        # No devices found i.e. len(device_list) = 0 OR
        # Multiple devices found i.e. len(device_list) ≥ 1
        raise ValueError(f"Expected exactly 1 device, but found {len(device_list)}")

    # AXES: Prepare two axes for use

    # Zaber Motion axes are indexed from 1
    x = device.get_axis(1)
    y = device.get_axis(2)

    # Home axes if needed
    if not x.is_homed():
        x.home()
    if not y.is_homed():
        y.home()

    # PARAMETERS: The system will scan a square area defined by two corners (start & end)

    # Define the starting coordinates
    x_start = 0  # mm
    y_start = 0  # mm

    # Define the end coordinates
    x_end = 100  # mm
    y_end = 100  # mm

    # Define the scan speed & step size between adjacent rows
    speed = 1  # mm/s
    step = 10  # mm

    # RASTER: Move in a raster scan pattern

    # Move to the starting position
    x.move_absolute(position=x_start, unit="mm")
    y.move_absolute(position=y_start, unit="mm")

    while x.get_position() <= x_end:
        # Move the y-axis from START to END coordinates
        while y_start <= y.get_position() <= y_end:
            # Move the y-axis at the specified speed
            y.move_velocity(velocity=speed, unit="mm/s")

        # Reset y-axis to start coordinate
        y.move_absolute(position=y_start, unit="mm")

        # Increment x-axis to scan the next row
        x.move_relative(step, "mm")

    # End of the program
    print("Raster scan complete")
