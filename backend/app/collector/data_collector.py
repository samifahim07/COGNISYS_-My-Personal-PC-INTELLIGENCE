
import json
import time

from backend.app.collector.system_monitor import get_system_metrics
from backend.app.database.connection import get_connection, initialize_database


def save_metrics(metrics):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO system_metrics (
            timestamp,
            cpu_usage_percent,
            cpu_frequency_mhz,
            ram_total_gb,
            ram_used_gb,
            ram_available_gb,
            ram_usage_percent,
            disk_read_gb,
            disk_write_gb,
            disks_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        metrics["timestamp"],
        metrics["cpu"]["usage_percent"],
        metrics["cpu"]["frequency_mhz"],
        metrics["ram"]["total_gb"],
        metrics["ram"]["used_gb"],
        metrics["ram"]["available_gb"],
        metrics["ram"]["usage_percent"],
        metrics["disk"]["read_gb"],
        metrics["disk"]["write_gb"],
        json.dumps(metrics["disk"]["partitions"])
    ))

    connection.commit()
    connection.close()


def start_collection(interval=10):

    initialize_database()

    print("\nCOGNISYS DATA COLLECTION STARTED")
    print("Collection interval: 10 seconds")
    print("Press CTRL + C to stop.\n")

    try:

        while True:

            metrics = get_system_metrics()

            save_metrics(metrics)

            print(
                f"Saved | "
                f"CPU: {metrics['cpu']['usage_percent']}% | "
                f"RAM: {metrics['ram']['usage_percent']}%"
            )

            time.sleep(interval)

    except KeyboardInterrupt:

        print("\nCOGNISYS DATA COLLECTION STOPPED.")


if __name__ == "__main__":
    start_collection()
