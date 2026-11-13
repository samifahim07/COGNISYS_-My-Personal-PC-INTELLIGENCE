
import ctypes
import threading
import psutil

from datetime import datetime

from backend.app.database.connection import (
    get_connection,
    initialize_database
)


# Windows foreground-window API
user32 = ctypes.WinDLL("user32", use_last_error=True)

user32.GetForegroundWindow.restype = ctypes.c_void_p

user32.GetWindowThreadProcessId.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_ulong)
]


def get_active_application():

    window_handle = user32.GetForegroundWindow()

    if not window_handle:
        return None

    process_id = ctypes.c_ulong()

    user32.GetWindowThreadProcessId(
        window_handle,
        ctypes.byref(process_id)
    )

    try:

        process = psutil.Process(process_id.value)

        return {
            "pid": process.pid,
            "name": process.name()
        }

    except (
        psutil.NoSuchProcess,
        psutil.AccessDenied,
        psutil.ZombieProcess
    ):
        return None


def save_application_session(
    application_name,
    process_id,
    start_time,
    end_time
):

    duration = (end_time - start_time).total_seconds()

    if duration <= 0:
        return

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO application_sessions (
                application_name,
                process_id,
                start_time,
                end_time,
                duration_seconds
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            application_name,
            process_id,
            start_time.isoformat(),
            end_time.isoformat(),
            duration
        ))

        connection.commit()

        print(
            f"Application Saved: {application_name} | "
            f"Duration: {duration:.1f}s"
        )

    finally:
        connection.close()


def start_usage_tracking(interval=5, stop_event=None):

    if stop_event is None:
        stop_event = threading.Event()

    initialize_database()

    print("\nCOGNISYS APPLICATION TRACKING STARTED")

    current_application = None
    session_start = None

    try:

        while not stop_event.is_set():

            application = get_active_application()
            current_time = datetime.now()

            if application is None:

                if current_application:

                    save_application_session(
                        current_application["name"],
                        current_application["pid"],
                        session_start,
                        current_time
                    )

                    current_application = None
                    session_start = None

            elif (
                current_application is None
                or application["pid"] != current_application["pid"]
            ):

                if current_application:

                    save_application_session(
                        current_application["name"],
                        current_application["pid"],
                        session_start,
                        current_time
                    )

                current_application = application
                session_start = current_time

                print(
                    f"Active Application: {application['name']}"
                )

            stop_event.wait(interval)

    except Exception as error:

        print(f"Application Tracker Error: {error}")

    finally:

        if current_application and session_start:

            save_application_session(
                current_application["name"],
                current_application["pid"],
                session_start,
                datetime.now()
            )

        print("Application tracker stopped safely.")


if __name__ == "__main__":

    start_usage_tracking()
