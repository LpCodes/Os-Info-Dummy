import platform

import psutil


SIZE_UNITS = {
    0: "B",
    1: "KB",
    2: "MB",
    3: "GB",
    4: "TB"
}


def convert_bytes(bytes):
    """ Converts bytes to a human-readable format """

    # Find the appropriate unit for the given bytes
    unit = 0
    while bytes >= 1024 and unit < len(SIZE_UNITS) - 1:
        bytes /= 1024
        unit += 1

    # Return the formatted string
    return f"{round(bytes, 2)} {SIZE_UNITS[unit]}"


def get_system_info():
    """ Gets detailed system information """

    try:
        # Get the basic system information
        system_name = platform.system()
        node_name = platform.node()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()

        # Get the CPU and memory information
        number_of_processors = psutil.cpu_count()
        memory = psutil.virtual_memory()
        disk_space = psutil.disk_usage("/")

        # Get the operating system architecture
        architecture = platform.architecture()[0]

        # Get the network information
        network_info = psutil.net_if_addrs()

        # Get the additional information
        battery_status = psutil.sensors_battery()
        boot_time = psutil.boot_time()
        current_cpu_usage = psutil.cpu_percent()

        # Print the basic system information
        print("System name:", system_name)
        print("Node name:", node_name)
        print("Release:", release)
        print("Version:", version)
        print("Machine:", machine)
        print("Processor:", processor)

        # Print the CPU and memory information
        print("Number of processors:", number_of_processors)
        print(
            f"Memory: {convert_bytes(memory.total)} (free: {convert_bytes(memory.available)}, used: "
            f"{convert_bytes(memory.used)})")
        print(
            f"Disk space: {convert_bytes(disk_space.total)} (free: {convert_bytes(disk_space.free)},"
            f" used: {convert_bytes(disk_space.used)})")

        # Print the operating system architecture
        print("Operating system architecture:", architecture)

        # Print the network information
        print("Network information:")
        for interface, addresses in network_info.items():
            print(f"Interface: {interface}")
            for address in addresses:
                print(f"- IP: {address.address}")
                print(f" Netmask: {address.netmask}")
                print(f" Broadcast IP: {address.broadcast}")

        # Print the additional information
        if battery_status:
            print(f"Battery status: {battery_status.percent}%")
            if battery_status.power_plugged:
                print("Power source: AC")
            else:
                print("Power source: Battery")
        else:
            print("Battery status: N/A")
        print(f"Boot time: {boot_time}")
        print(f"Current CPU usage: {current_cpu_usage}%")

    except Exception as e:
        print("An error occurred while retrieving system information:", str(e))


if __name__ == "__main__":
    get_system_info()
