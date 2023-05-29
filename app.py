import platform
import psutil

def convert_bytes(bytes):
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes >= 1024 and i < len(sizes) - 1:
        bytes /= 1024
        i += 1
    return f"{round(bytes, 2)} {sizes[i]}"

def get_system_info():
    """ Gets detailed system information """

    try:
        system_name = platform.system()
        node_name = platform.node()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()
        number_of_processors = psutil.cpu_count()
        memory = convert_bytes(psutil.virtual_memory().total)
        disk_space = convert_bytes(psutil.disk_usage("/").total)
        architecture = platform.architecture()[0]
        free_memory = convert_bytes(psutil.virtual_memory().available)
        used_memory = convert_bytes(psutil.virtual_memory().used)
        free_disk_space = convert_bytes(psutil.disk_usage("/").free)
        used_disk_space = convert_bytes(psutil.disk_usage("/").used)
        network_info = psutil.net_if_addrs()

        print("System name:", system_name)
        print("Node name:", node_name)
        print("Release:", release)
        print("Version:", version)
        print("Machine:", machine)
        print("Processor:", processor)
        print("Number of processors:", number_of_processors)
        print("Memory:", memory)
        print("Disk space:", disk_space)
        print("Operating system architecture:", architecture)
        print("Free memory:", free_memory)
        print("Used memory:", used_memory)
        print("Free disk space:", free_disk_space)
        print("Used disk space:", used_disk_space)
        print("Network information:")
        for interface, addresses in network_info.items():
            print(f"Interface: {interface}")
            for address in addresses:
                print(f"- IP: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")

    except Exception as e:
        print("An error occurred while retrieving system information:", str(e))


if __name__ == "__main__":
    get_system_info()
