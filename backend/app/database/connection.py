
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

    # Table 1: System performance history
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

    # Table 2: Application usage sessions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS application_sessions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            application_name TEXT NOT NULL,
            process_id INTEGER,

            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,

            duration_seconds REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()

    print("\n========== COGNISYS DATABASE ==========\n")
    print("Database initialized successfully!")
    print(f"Database location: {DATABASE_PATH}")
    print("Table 1: system_metrics")
    print("Table 2: application_sessions")


if __name__ == "__main__":

    initialize_database()
