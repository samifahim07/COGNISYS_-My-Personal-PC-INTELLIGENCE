
import time
import threading

from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

from backend.app.collector.data_collector import start_collection
from backend.app.collector.usage_tracker import start_usage_tracking


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOG_PATH = PROJECT_ROOT / "logs" / "cognisys.log"


def start_cognisys():

    LOG_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(LOG_PATH, "a", encoding="utf-8", buffering=1) as log_file:

        with redirect_stdout(log_file), redirect_stderr(log_file):

            print("\n========== COGNISYS STARTED ==========")

            print("Starting system monitoring...")
            print("Starting application tracking...")

            # System monitoring thread
            system_thread = threading.Thread(
                target=start_collection,
                kwargs={"interval": 10},
                daemon=True
            )

            # Application tracking thread
            usage_thread = threading.Thread(
                target=start_usage_tracking,
                kwargs={"interval": 5},
                daemon=True
            )

            system_thread.start()
            usage_thread.start()

            print("Both collectors are running.")

            try:

                while True:
                    time.sleep(1)

            except KeyboardInterrupt:

                print("COGNISYS stopped manually.")


if __name__ == "__main__":

    start_cognisys()
