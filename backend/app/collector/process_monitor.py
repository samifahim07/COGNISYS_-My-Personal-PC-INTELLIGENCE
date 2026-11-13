
import psutil


def get_running_processes():

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_info"]
    ):

        try:
            info = process.info

            memory = info["memory_info"]

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu_percent": info["cpu_percent"],
                "memory_mb": round(
                    memory.rss / (1024 * 1024), 2
                ) if memory else 0
            })

        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            continue

    processes.sort(
        key=lambda item: item["memory_mb"],
        reverse=True
    )

    return processes


if __name__ == "__main__":

    running_apps = get_running_processes()

    print("\n========== COGNISYS PROCESS MONITOR ==========\n")

    for app in running_apps[:15]:

        print(
            f"PID: {app['pid']} | "
            f"App: {app['name']} | "
            f"RAM: {app['memory_mb']} MB | "
            f"CPU: {app['cpu_percent']}%"
        )
