import platform
import psutil
import argparse
import json
from datetime import datetime, timedelta
import GPUtil
from colorama import init, Fore, Style

# Initialize colorama
init()

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

    # Return the formatted strings
    return f"{round(bytes, 2)} {SIZE_UNITS[unit]}"


def get_uptime():
    """ Get system uptime in human-readable format """
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"


def get_gpu_info():
    """ Get GPU information """
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                "id": gpu.id,
                "name": gpu.name,
                "load": f"{gpu.load*100}%",
                "memory_used": f"{gpu.memoryUsed}MB",
                "memory_total": f"{gpu.memoryTotal}MB",
                "temperature": f"{gpu.temperature}°C"
            })
        return gpu_info
    except Exception as e:
        return f"GPU information not available: {str(e)}"


def get_disk_partitions():
    """ Get detailed disk partition information """
    try:
        partitions = psutil.disk_partitions()
        partition_info = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": convert_bytes(usage.total),
                "used": convert_bytes(usage.used),
                "free": convert_bytes(usage.free),
                "percent": f"{usage.percent}%"
            })
        return partition_info
    except Exception as e:
        return f"Disk partition information not available: {str(e)}"


def get_process_info():
    """ Get top processes by CPU usage """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:5]
    except Exception as e:
        return f"Process information not available: {str(e)}"


def get_temperature_info():
    """ Get system temperature information """
    try:
        if hasattr(psutil, 'sensors_temperatures'):
            temps = psutil.sensors_temperatures()
            temp_info = {}
            for name, entries in temps.items():
                temp_info[name] = [{"current": entry.current, "high": entry.high, "critical": entry.critical} 
                                 for entry in entries]
            return temp_info
        else:
            return "Temperature sensors not available on this system"
    except Exception as e:
        return f"Temperature information not available: {str(e)}"


def get_system_info(json_output=False):
    """ Gets detailed system information """
    info = {}
    
    try:
        # Basic system information
        info["system"] = {
            "name": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0]
        }

        # CPU and memory information
        info["cpu"] = {
            "count": psutil.cpu_count(),
            "usage": f"{psutil.cpu_percent()}%",
            "freq": f"{psutil.cpu_freq().current}MHz"
        }

        memory = psutil.virtual_memory()
        info["memory"] = {
            "total": convert_bytes(memory.total),
            "available": convert_bytes(memory.available),
            "used": convert_bytes(memory.used),
            "percent": f"{memory.percent}%"
        }

        # Disk information
        info["disk"] = {
            "partitions": get_disk_partitions()
        }

        # Network information
        network_info = {}
        for interface, addresses in psutil.net_if_addrs().items():
            network_info[interface] = [{
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast
            } for addr in addresses]
        info["network"] = network_info

        # Additional information
        info["additional"] = {
            "uptime": get_uptime(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            "gpu": get_gpu_info(),
            "temperature": get_temperature_info(),
            "top_processes": get_process_info()
        }

        # Battery information
        battery = psutil.sensors_battery()
        if battery:
            info["battery"] = {
                "percent": f"{battery.percent}%",
                "power_plugged": battery.power_plugged,
                "secsleft": battery.secsleft if battery.secsleft != -1 else "Unknown"
            }

        if json_output:
            return json.dumps(info, indent=4)
        else:
            return format_output(info)

    except Exception as e:
        return f"An error occurred while retrieving system information: {str(e)}"


def format_output(info):
    """ Format the output in a readable way with colors """
    output = []
    
    # System Information
    output.append(f"{Fore.CYAN}=== System Information ==={Style.RESET_ALL}")
    for key, value in info["system"].items():
        output.append(f"{Fore.GREEN}{key.title()}:{Style.RESET_ALL} {value}")

    # CPU and Memory
    output.append(f"\n{Fore.CYAN}=== CPU and Memory ==={Style.RESET_ALL}")
    for key, value in info["cpu"].items():
        output.append(f"{Fore.GREEN}{key.title()}:{Style.RESET_ALL} {value}")
    for key, value in info["memory"].items():
        output.append(f"{Fore.GREEN}{key.title()}:{Style.RESET_ALL} {value}")

    # Disk Information
    output.append(f"\n{Fore.CYAN}=== Disk Information ==={Style.RESET_ALL}")
    for partition in info["disk"]["partitions"]:
        output.append(f"\n{Fore.YELLOW}Partition: {partition['device']}{Style.RESET_ALL}")
        for key, value in partition.items():
            if key != "device":
                output.append(f"{Fore.GREEN}{key.title()}:{Style.RESET_ALL} {value}")

    # Network Information
    output.append(f"\n{Fore.CYAN}=== Network Information ==={Style.RESET_ALL}")
    for interface, addresses in info["network"].items():
        output.append(f"\n{Fore.YELLOW}Interface: {interface}{Style.RESET_ALL}")
        for addr in addresses:
            for key, value in addr.items():
                if value:
                    output.append(f"{Fore.GREEN}{key.title()}:{Style.RESET_ALL} {value}")

    # Additional Information
    output.append(f"\n{Fore.CYAN}=== Additional Information ==={Style.RESET_ALL}")
    for key, value in info["additional"].items():
        output.append(f"\n{Fore.YELLOW}{key.title()}:{Style.RESET_ALL}")
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        output.append(f"{Fore.GREEN}{k.title()}:{Style.RESET_ALL} {v}")
                else:
                    output.append(str(item))
        else:
            output.append(str(value))

    # Battery Information
    if "battery" in info:
        output.append(f"\n{Fore.CYAN}=== Battery Information ==={Style.RESET_ALL}")
        for key, value in info["battery"].items():
            output.append(f"{Fore.GREEN}{key.title()}:{Style.RESET_ALL} {value}")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="System Information Tool")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    result = get_system_info(json_output=args.json)
    print(result)


if __name__ == "__main__":
    main()
