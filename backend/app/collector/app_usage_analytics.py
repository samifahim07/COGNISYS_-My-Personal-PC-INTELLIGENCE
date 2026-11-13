from backend.app.database.connection import get_connection


def get_usage_report():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            application_name,
            COUNT(*) AS total_sessions,
            SUM(duration_seconds) AS total_duration

        FROM application_sessions

        GROUP BY application_name

        ORDER BY total_duration DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def format_duration(seconds):

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return (
        f"{hours}h {minutes}m {remaining_seconds}s"
    )


if __name__ == "__main__":

    report = get_usage_report()

    print("\n========== COGNISYS USAGE ANALYTICS ==========\n")

    if not report:

        print("No application usage data found.")

    else:

        for app_name, sessions, duration in report:

            print(f"Application: {app_name}")
            print(f"Sessions: {sessions}")
            print(f"Total Usage: {format_duration(duration)}")
            print("----------------------------------------")