"""
This example script demonstrates how to use the Micro Epsilon Data Acquisition Library (MEDAQLib). Requires a connected
Micro Epsilon sensor. See https://www.micro-epsilon.co.uk/service/software-sensorintegration/ for more information.

The program:
    1. Establishes connection with the sensor
    2. Reads data from the sensor
    4. Handles alerts and disconnection events

Raises:
    ValueError:
"""

import time

from microepsilon import MEDAQLib, ERR_CODE, SENSOR_TYPE


def check_error() -> None:
    """
    Every sensor function returns an error code. If the function
    succeeds, the `NO_ERROR` code is returned.

    The sensor maintains an internal list of error codes. Each time an
    action is taken, the sensor appends the resulting error code to
    this internal list. The internal list therefore provides a
    chronological record of all successful and unsuccessful actions
    performed by the sensor. For improved robustness, Micro Epsilon
    recommends checking the error code after each function call.

    This helper function reads the most recent error code from the
    internal list using `GetLastError`, raising a `ValueError` if the
    result is not `NO_ERROR`. A detailed error description (string)
    is retrieved using `GetError` for informative debugging.

    :raises ValueError: If the sensor detects an error. The exception
        message contains the error message retrieved from the sensor.
    :return: None
    """
    if sensor.GetLastError() != ERR_CODE.NO_ERROR:
        # Print the OpenSensor Error message
        raise ValueError(sensor.GetError())


# SETUP: Tell MEDAQLib about the sensor

# Specify the sensor type
sensor = MEDAQLib.CreateSensorInstance(SENSOR_TYPE.SENSOR_IFC2421)

# Specify the communication interface
sensor.SetParameterString("IP_Interface", "TCP/IP")
sensor.SetParameterString("IP_RemoteAddr", "169.254.168.150")

# OPTIONAL: Adjust sensor settings

# Enable Logfile writing
sensor.SetParameterInt("IP_EnableLogging", 1)

# Enable automatic MEDAQLib and sensor setup
sensor.SetParameterInt("IP_AutomaticMode", 3)

# DETECT: Find the Micro Epsilon sensor

# Open the specified connection
sensor.OpenSensor()

# Check the latest error code from OpenSensor
check_error()

# Operation succeeded (no error)
print("Successfully opened sensor instance")

# READ: Read data from the sensor

# Set the number of measurements to read
# Use n > 1 if averaging is required
n = 1

if not n.is_integer() or not 0 < n <= 10:
    # Raise an exception if the user specifies an invalid value for n
    raise ValueError("n must be a positive integer between 1 and 10")

# Check if the sensor is ready to send data
while not sensor.DataAvail() > n:
    # Check the latest error code from DataAvail
    check_error()
    print("Waiting for sensor data")
    time.sleep(0.1)

# Get the most recent n measurements from the sensor
poll_data = sensor.Poll(n)

# Check the latest error code from Poll
check_error()

# Report the data
print(f"\nPolled {n} data:\n", poll_data)

# Bulk transfer data out of the MEDAQLib internal buffer
transferred_data = sensor.TransferData(n)
print(f"\nTransferred {n} data:\n", transferred_data)

# SHUTDOWN: Tidy up resources

# Close the communication interface
sensor.CloseSensor()

# Release the sensor
sensor.ReleaseSensorInstance()

# End of program
print("Sensor test complete")
