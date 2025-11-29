import platform
import psutil
import ctypes

# Function to get full installed RAM
def get_installed_ram_gb():
    try:
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong)
            ]
        memoryStatus = MEMORYSTATUSEX()
        memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
        return round(memoryStatus.ullTotalPhys / (1024**3), 2)
    except:
        # fallback if ctypes fails
        return round(psutil.virtual_memory().total / (1024**3), 2)

# Collect system info
mem = psutil.virtual_memory()

info = {
    "OS": platform.system() + " " + platform.release(),
    "OS Version": platform.version(),
    "Machine": platform.machine(),
    "Processor": platform.processor(),
    "CPU Cores": psutil.cpu_count(logical=False),
    "Logical CPUs": psutil.cpu_count(logical=True),
    "Installed RAM": f"{get_installed_ram_gb()} GB",
    "Usable RAM": f"{round(mem.total / (1024**3), 2)} GB",
    "RAM Used": f"{round(mem.used / (1024**3), 2)} GB",
    "RAM Available": f"{round(mem.available / (1024**3), 2)} GB",
    "RAM Usage %": f"{mem.percent}%"
}

# Add all disk drives
for partition in psutil.disk_partitions():
    usage = psutil.disk_usage(partition.mountpoint)
    info[f"{partition.device} Total"] = f"{round(usage.total / (1024**3), 2)} GB"
    info[f"{partition.device} Used"] = f"{round(usage.used / (1024**3), 2)} GB"
    info[f"{partition.device} Free"] = f"{round(usage.free / (1024**3), 2)} GB"
    info[f"{partition.device} Usage %"] = f"{usage.percent}%"

# Generate HTML report
report_file = "report.html"
with open(report_file, "w", encoding="utf-8") as f:
    f.write("<html><body style='font-family: Arial;'>")
    f.write("<h1>System Information Report</h1>")
    f.write("<table border='1' style='border-collapse: collapse;'>")

    for key, value in info.items():
        color = ""
        # Highlight low disk space
        if "Free" in key and float(value.split()[0]) < 10:
            color = "red"
        # Highlight high RAM usage
        if key == "RAM Usage %" and float(value.strip('%')) > 90:
            color = "red"
        f.write(f"<tr><td>{key}</td><td style='color:{color}'>{value}</td></tr>")

    f.write("</table></body></html>")

print("System info report generated! Open report.html to view it.")
