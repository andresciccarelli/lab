import os
import platform
import subprocess
import re
from datetime import datetime

def get_uptime():
    system = platform.system()
    if system == "Linux":
        try:
            with open("/proc/uptime") as f:
                uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            seconds = int(uptime_seconds % 60)
            return f"System uptime: {hours}h {minutes}m {seconds}s"
        except (OSError, ValueError, IndexError) as e:
            return f"Could not determine uptime: {e}"
    elif system == "Darwin":
        try:
            # Avoid shell=True for safety
            output = subprocess.check_output(["uptime"], text=True)
            # Regex for 'up' time string
            match = re.search(r"up\s+(.*?),\s+\d+\s+user", output)
            if match:
                return f"System uptime: {match.group(1)}"
            else:
                return "Could not determine uptime"
        except subprocess.CalledProcessError as e:
            return f"Could not determine uptime: {e}"
    elif system == "Windows":
        try:
            # Use 'systeminfo' for more reliability, avoid shell=True and decode
            output = subprocess.check_output(
                ["systeminfo"], text=True, encoding="utf-8", errors="ignore"
            )
            for line in output.splitlines():
                if "System Boot Time" in line or "System Up Time" in line:
                    # Extract boot time or up time, depending on Windows language
                    boot_line = line.split(":", 1)[-1].strip()
                    return f"System boot time: {boot_line}"
            return "Could not determine uptime"
        except subprocess.CalledProcessError as e:
            return f"Could not determine uptime: {e}"
    else:
        return "Unsupported OS"

if __name__ == "__main__":
    print(get_uptime())