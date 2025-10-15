"""

"""

from OceanDirect import OceanDirectAPI, OceanDirectError

# SETUP

# Initialise the Ocean Direct API
od = OceanDirectAPI()

# Display API version
api_version = od.get_api_version_numbers()
print(f"API Version : {api_version[0]}.{api_version[1]}.{api_version[2]}")

# DETECT

# Search for connected devices
if not od.find_usb_devices() > 0:
    print("No devices found.")
    exit(0)

# Get the device ID list
device_ids = od.get_device_ids()

# CONNECT

# Open a connection with the first device
device = od.open_device(device_ids[0])

# Display device ID
print(f"Device ID : {device_ids[0]}")

# REPORT

try:
    # Serial number
    serial_number = device.get_serial_number()
    print(f"Serial Number : {serial_number}")
except OceanDirectError as err:
    # Catch error
    print(f"Serial Number Error : {err.get_error_details()}")

try:
    # Firmware version
    firmware_version = device.Advanced.get_revision_firmware()
    print(f"Firmware Version : {firmware_version}")
except OceanDirectAPI.OceanDirectError as err:
    # Catch error
    print(f"Firmware Version Error : {err.get_error_details()}")

try:
    # FPGA version
    fpga_version = device.Advanced.get_revision_fpga()
    print(f"FPGA Version : {fpga_version}")
except OceanDirectError as err:
    # Catch error
    print(f"FPGA Version Error : {err.get_error_details()}")

# SHUTDOWN

# Close the connection
od.close_device(device_ids[0])

# Close the Ocean Direct API
od.shutdown()
