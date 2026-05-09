import time
import psutil
import subprocess
import platform
import re
import os
from datetime import datetime

# =========================
# CONFIG
# =========================

TOPSIDE_IP = "192.168.1.1"   # CHANGE THIS
NETWORK_INTERFACE = "eth0"    # CHANGE if needed

PING_INTERVAL = 2
SYSTEM_INTERVAL = 1

LOG_DIR = "/home/mamorobotics/rov_logs"

# =========================
# CREATE LOG DIRECTORY
# =========================

os.makedirs(LOG_DIR, exist_ok=True)

# =========================
# CREATE SESSION LOG FILE
# =========================

session_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

LOGFILE = os.path.join(
    LOG_DIR,
    f"rov_session_{session_time}.log"
)

# =========================
# LOGGING FUNCTION
# =========================

def log(message):

    timestamp = datetime.now().isoformat()

    line = f"{timestamp} | {message}"

    print(line)

    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

# =========================
# TEMPERATURE
# =========================

def get_temp():

    try:
        out = subprocess.check_output(
            ["vcgencmd", "measure_temp"]
        ).decode().strip()

        return out

    except Exception as e:
        return f"temp_error={e}"

# =========================
# THROTTLING STATUS
# =========================

def get_throttled():

    try:
        out = subprocess.check_output(
            ["vcgencmd", "get_throttled"]
        ).decode().strip()

        return out

    except Exception as e:
        return f"throttle_error={e}"

# =========================
# NETWORK PING
# =========================

def ping_host(ip):

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", ip]

    try:

        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            timeout=2
        ).decode()

        latency_match = re.search(
            r'time=([\d.]+)\s*ms',
            output
        )

        latency = (
            latency_match.group(1)
            if latency_match else "unknown"
        )

        return True, latency

    except Exception:

        return False, None

# =========================
# NETWORK INTERFACE STATS
# =========================

def get_network_stats(interface):

    try:

        stats = psutil.net_io_counters(pernic=True)

        if interface not in stats:
            return "interface_missing"

        net = stats[interface]

        return (
            f"TX={net.bytes_sent} "
            f"RX={net.bytes_recv} "
            f"TXpkts={net.packets_sent} "
            f"RXpkts={net.packets_recv} "
            f"ERRin={net.errin} "
            f"ERRout={net.errout} "
            f"DROPin={net.dropin} "
            f"DROPout={net.dropout}"
        )

    except Exception as e:

        return f"net_error={e}"

# =========================
# START LOGGING
# =========================

log("===================================")
log("ROV Monitor Started")
log(f"Session Log: {LOGFILE}")
log("===================================")

last_ping = 0

while True:

    now = time.time()

    # -------------------------
    # SYSTEM HEALTH
    # -------------------------

    cpu = psutil.cpu_percent()

    ram = psutil.virtual_memory().percent

    temp = get_temp()

    throttled = get_throttled()

    log(
        f"SYSTEM "
        f"CPU={cpu}% "
        f"RAM={ram}% "
        f"{temp} "
        f"{throttled}"
    )

    # -------------------------
    # NETWORK CHECK
    # -------------------------

    if now - last_ping >= PING_INTERVAL:

        connected, latency = ping_host(TOPSIDE_IP)

        net_stats = get_network_stats(NETWORK_INTERFACE)

        if connected:

            log(
                f"NETWORK "
                f"PING_OK "
                f"latency={latency}ms "
                f"{net_stats}"
            )

        else:

            log(
                f"NETWORK "
                f"PING_FAIL "
                f"{net_stats}"
            )

        last_ping = now

    time.sleep(SYSTEM_INTERVAL)