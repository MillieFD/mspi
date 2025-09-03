from zaber_motion import Units
from zaber_motion.ascii import Connection

with Connection.open_serial_port("dev/tty/USB0") as connection:
    connection.alert.subscribe(lambda alert: print('Alert:', alert))
    connection.disconnected.subscribe(lambda err: print('Disconnected:', err))

    connection.enable_alerts()

    device_list = connection.detect_devices()

    # Try to unpack the list into a single device
    try:
        device, = device_list
        axis = device.get_axis(1)
        if not axis.is_homed():
            axis.home()
        # Move to 10 mm
        axis.move_absolute(10, Units.LENGTH_MILLIMETRES)
        # Move by an additional 5 mm
        axis.move_relative(5, Units.LENGTH_MILLIMETRES)
    except ValueError:
        raise ValueError(f"Expected exactly 1 device, but found {len(device_list)}")