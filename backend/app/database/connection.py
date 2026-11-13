
import sqlite3
from pathlib import Path


# Find the main project directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Database location
DATABASE_PATH = PROJECT_ROOT / "data" / "cognisys.db"


def get_connection():

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            cpu_usage_percent REAL,
            cpu_frequency_mhz REAL,

            ram_total_gb REAL,
            ram_used_gb REAL,
            ram_available_gb REAL,
            ram_usage_percent REAL,

            disk_read_gb REAL,
            disk_write_gb REAL,

            disks_json TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("COGNISYS DATABASE INITIALIZED!")
    print(f"Database location: {DATABASE_PATH}")


if __name__ == "__main__":
    initialize_database()
