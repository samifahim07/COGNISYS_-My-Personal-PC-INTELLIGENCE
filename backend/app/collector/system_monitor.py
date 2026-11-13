
import psutil
import json
from datetime import datetime


def get_system_metrics():

    # CPU information
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_frequency = psutil.cpu_freq()

    # RAM information
    memory = psutil.virtual_memory()

    # Disk I/O information
    disk_io = psutil.disk_io_counters()

    # Disk partition information
    disks = []

    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            disks.append({
                "drive": partition.mountpoint,
                "total_gb": round(usage.total / (1024 ** 3), 2),
                "used_gb": round(usage.used / (1024 ** 3), 2),
                "free_gb": round(usage.free / (1024 ** 3), 2),
                "usage_percent": usage.percent
            })

        except PermissionError:
            continue

    # Collect all metrics
    metrics = {
        "timestamp": datetime.now().isoformat(),

        "cpu": {
            "usage_percent": cpu_usage,
            "frequency_mhz": (
                round(cpu_frequency.current, 2)
                if cpu_frequency else None
            )
        },

        "ram": {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2),
            "usage_percent": memory.percent
        },

        "disk": {
            "read_gb": (
                round(disk_io.read_bytes / (1024 ** 3), 4)
                if disk_io else None
            ),
            "write_gb": (
                round(disk_io.write_bytes / (1024 ** 3), 4)
                if disk_io else None
            ),
            "partitions": disks
        }
    }

    return metrics


if __name__ == "__main__":

    data = get_system_metrics()

    print("\n========== COGNISYS SYSTEM MONITOR ==========\n")
    print(json.dumps(data, indent=4))
