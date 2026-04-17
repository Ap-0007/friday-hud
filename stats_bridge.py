import psutil
import json
import time
import os

STATS_FILE = os.path.join(os.path.dirname(__file__), "system_stats.json")

def get_stats():
    battery = psutil.sensors_battery()
    return {
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "battery": battery.percent if battery else 100,
        "charging": battery.power_plugged if battery else True,
        "timestamp": time.time()
    }

def main():
    print("F.R.I.D.A.Y. Heartbeat Monitor Started.")
    print(f"Writing stats to {STATS_FILE}...")
    try:
        while True:
            stats = get_stats()
            with open(STATS_FILE, "w") as f:
                json.dump(stats, f)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nHeartbeat monitor offline.")

if __name__ == "__main__":
    main()
