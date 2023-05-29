import platform
import psutil


def get_system_info():
    """Gets detailed system information."""

    # Get the system name.
    system_name = platform.system()

    # Get the node name.
    node_name = platform.node()

    # Get the release.
    release = platform.release()

    # Get the version.
    version = platform.version()

    # Get the machine.
    machine = platform.machine()

    # Get the processor.
    processor = platform.processor()

    # Get the number of processors.
    number_of_processors = psutil.cpu_count()

    # Get the memory.
    memory = round(psutil.virtual_memory().total / 1024 ** 3)

    # Get the disk space.
    disk_space = round(psutil.disk_usage("/").total / 1024 ** 3, 2)

    # Get the operating system architecture.
    architecture = platform.architecture()[0]

    # Get the amount of free memory.
    free_memory = round(psutil.virtual_memory().free / 1024 ** 3, 2)

    # Get the amount of used memory.
    used_memory = round(memory - free_memory, 2)

    # Get the amount of free disk space.
    free_disk_space = round(psutil.disk_usage("/").free / 1024 ** 3, 2)

    # Get the amount of used disk space.
    used_disk_space = round(disk_space - free_disk_space, 2)

    # Get the network information.
    network_info = psutil.net_if_addrs()

    # Print the system information.
    print("System name:", system_name)
    print("Node name:", node_name)
    print("Release:", release)
    print("Version:", version)
    print("Machine:", machine)
    print("Processor:", processor)
    print("Number of processors:", number_of_processors)
    print("Memory:", memory, "GB")
    print("Disk space:", disk_space, "GB")
    print("Operating system architecture:", architecture)
    print("Free memory:", free_memory, "GB")
    print("Used memory:", used_memory, "GB")
    print("Free disk space:", free_disk_space, "GB")
    print("Used disk space:", used_disk_space, "GB")
    print("Network information:")
    for interface, addresses in network_info.items():
        print(f"Interface: {interface}")
        for address in addresses:
            print(f"- IP: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")


if __name__ == "__main__":
    get_system_info()
