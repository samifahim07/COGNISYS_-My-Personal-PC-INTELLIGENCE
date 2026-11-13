
import threading
import msvcrt

from pathlib import Path

from backend.app.collector.data_collector import start_collection
from backend.app.collector.usage_tracker import start_usage_tracking


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOCK_PATH = PROJECT_ROOT / "data" / "cognisys.lock"


def acquire_lock():

    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)

    lock_file = open(LOCK_PATH, "a+b")

    if LOCK_PATH.stat().st_size == 0:
        lock_file.write(b"0")
        lock_file.flush()

    lock_file.seek(0)

    try:
        msvcrt.locking(
            lock_file.fileno(),
            msvcrt.LK_NBLCK,
            1
        )

        return lock_file

    except OSError:
        lock_file.close()
        return None


def release_lock(lock_file):

    if lock_file is not None:

        try:
            lock_file.seek(0)

            msvcrt.locking(
                lock_file.fileno(),
                msvcrt.LK_UNLCK,
                1
            )

        finally:
            lock_file.close()


def start_cognisys():

    lock_file = acquire_lock()

    if lock_file is None:

        print("\nCOGNISYS IS ALREADY RUNNING!")
        print("Only one instance is allowed.")
        return

    stop_event = threading.Event()

    print("\n========== COGNISYS ==========")
    print("COGNISYS is starting...")

    system_thread = threading.Thread(
        target=start_collection,
        kwargs={
            "interval": 10,
            "stop_event": stop_event
        }
    )

    usage_thread = threading.Thread(
        target=start_usage_tracking,
        kwargs={
            "interval": 5,
            "stop_event": stop_event
        }
    )

    try:

        system_thread.start()
        usage_thread.start()

        print("\nCOGNISYS IS RUNNING")
        print("System Monitor: RUNNING")
        print("Application Tracker: RUNNING")
        print("Press CTRL + C to stop safely.\n")

        while system_thread.is_alive() or usage_thread.is_alive():

            system_thread.join(timeout=0.5)
            usage_thread.join(timeout=0.5)

    except KeyboardInterrupt:

        print("\nCOGNISYS SHUTDOWN REQUESTED...")

        stop_event.set()

        system_thread.join()
        usage_thread.join()

        print("\nAll collectors stopped safely.")
        print("COGNISYS STOPPED.")

    finally:

        stop_event.set()

        if system_thread.is_alive():
            system_thread.join()

        if usage_thread.is_alive():
            usage_thread.join()

        release_lock(lock_file)


if __name__ == "__main__":

    start_cognisys()
