
import json
import threading

from backend.app.collector.system_monitor import get_system_metrics
from backend.app.database.connection import (
    get_connection,
    initialize_database
)


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


def start_collection(interval=10, stop_event=None):

    if stop_event is None:
        stop_event = threading.Event()

    initialize_database()

    print("\nCOGNISYS SYSTEM COLLECTION STARTED")
    print(f"Collection interval: {interval} seconds")

    while not stop_event.is_set():

        try:

            metrics = get_system_metrics()

            save_metrics(metrics)

            print(
                f"System Saved | "
                f"CPU: {metrics['cpu']['usage_percent']}% | "
                f"RAM: {metrics['ram']['usage_percent']}%"
            )

        except Exception as error:

            print(f"System Collector Error: {error}")

        stop_event.wait(interval)

    print("System collector stopped safely.")
