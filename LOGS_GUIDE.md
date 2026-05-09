# ROV Logging & Diagnostics Guide

This guide explains how to view and interpret logs on the Raspberry Pi inside the ROV.

The Raspberry Pi automatically records:

* camera streamer logs (`ustreamer`)
* system events
* USB disconnects
* crashes/restarts
* network interruptions
* undervoltage warnings
* temperature/throttling issues

These logs are extremely useful when diagnosing:

* frozen video feeds
* intermittent disconnects
* camera crashes
* Raspberry Pi instability
* tether/network issues

---

# Quick Overview

There are **two main types of logs**:

| Log Type            | Purpose                        |
| ------------------- | ------------------------------ |
| `journalctl` logs   | System/service logs from Linux |
| Python monitor logs | Custom ROV health logging      |

This guide focuses mainly on `journalctl`, since it captures:

* `ustreamer` output
* service crashes
* USB errors
* kernel messages
* reboot history

---

# Basic Linux Navigation

Open a terminal on the Raspberry Pi.

Most commands below are typed directly into the terminal.

---

# Viewing Live Camera Logs

To watch live logs from the front camera:

```bash id="5k6oqn"
journalctl -u ustreamer_front -f -o short-precise
```

To watch live logs from the bottom camera:

```bash id="jz0h68"
journalctl -u ustreamer_bottom -f -o short-precise
```

## What this does

| Part               | Meaning                      |
| ------------------ | ---------------------------- |
| `journalctl`       | Linux log viewer             |
| `-u`               | Selects a specific service   |
| `-f`               | “Follow” mode (live updates) |
| `-o short-precise` | Shows readable timestamps    |

---

# Example Output

```text id="fpjlwm"
2026-05-09 14:22:31.482193 EDT ustreamer[512]: Device connected
2026-05-09 14:22:32.019288 EDT ustreamer[512]: Stream started
```

---

# Viewing Logs From the Previous Boot

Very useful after:

* freezes
* crashes
* unexpected reboots
* power failures

Front camera:

```bash id="24wqqf"
journalctl -u ustreamer_front -b -1
```

Bottom camera:

```bash id="jlwm02"
journalctl -u ustreamer_bottom -b -1
```

## What `-b -1` Means

| Option | Meaning             |
| ------ | ------------------- |
| `-b`   | Select boot session |
| `-1`   | Previous boot       |

---

# Viewing System-Wide Errors

To view important system-level problems:

```bash id="cyzhtf"
journalctl -p warning
```

This shows:

* warnings
* errors
* hardware issues

---

# Viewing Kernel / USB Errors

Very important for diagnosing:

* camera disconnects
* USB instability
* tether adapter resets

```bash id="jlwmck"
journalctl -k -o short-precise
```

or:

```bash id="1h1lvc"
dmesg -T
```

---

# Common Things to Look For

## 1. Undervoltage Warnings

Example:

```text id="95jnn4"
Under-voltage detected!
```

This usually means:

* power supply instability
* voltage sag
* tether resistance
* buck converter problems

This is one of the most common causes of Raspberry Pi freezes.

---

## 2. USB Disconnects

Example:

```text id="v0l0np"
USB disconnect, device number 4
```

Possible causes:

* loose USB cable
* insufficient power
* electrical noise
* USB bandwidth overload

---

## 3. Camera Errors

Example:

```text id="4l9gsp"
Frame timeout
```

Possible causes:

* overloaded USB bus
* camera crash
* insufficient bandwidth

---

## 4. Service Restart Loops

Example:

```text id="owjlwm"
ustreamer.service: Scheduled restart job
```

This means Linux automatically restarted the video streamer after a crash.

---

# Viewing Only Recent Logs

Last 5 minutes:

```bash id="95l1lf"
journalctl --since "5 minutes ago"
```

Last hour:

```bash id="5pn18d"
journalctl --since "1 hour ago"
```

---

# Searching Logs

Search for USB messages:

```bash id="lp3fxz"
journalctl | grep USB
```

Search for errors:

```bash id="9qfdcq"
journalctl | grep error
```

Search for undervoltage warnings:

```bash id="e7l0yw"
journalctl | grep voltage
```

---

# Exiting Log View

Many log commands open an interactive viewer.

To exit:

* press `q`

---

# ROV Monitor Logs

The custom ROV monitor script stores logs in:

```text id="l65jca"
/home/pi/rov_logs/
```

Each run/session creates a separate log file.

Example:

```text id="vjlwmm"
rov_session_2026-05-09_14-02-51.log
```

---

# Viewing Monitor Logs

View the newest log file:

```bash id="4mjlwm"
ls -lt /home/pi/rov_logs
```

View a specific log:

```bash id="jlwmf7"
cat /home/pi/rov_logs/rov_session_2026-05-09_14-02-51.log
```

Follow updates live:

```bash id="2yjlwm"
tail -f /home/pi/rov_logs/rov_session_2026-05-09_14-02-51.log
```

---

# Interpreting Monitor Logs

Example:

```text id="q8by1t"
2026-05-09T14:02:52.102 | SYSTEM CPU=17.2% RAM=41.5% temp=48.0'C throttled=0x0
```

## Important Fields

| Field     | Meaning                  |
| --------- | ------------------------ |
| CPU       | CPU usage                |
| RAM       | Memory usage             |
| temp      | Raspberry Pi temperature |
| throttled | Power/thermal status     |

---

# Understanding `throttled=`

| Value     | Meaning                          |
| --------- | -------------------------------- |
| `0x0`     | No problems detected             |
| `0x1`     | Undervoltage happening now       |
| `0x10000` | Undervoltage occurred previously |
| `0x4`     | Thermal throttling happening now |

If anything besides `0x0` appears, power or thermal issues may exist.

---

# Recommended Debugging Process

When a freeze happens:

1. Check if the Raspberry Pi rebooted
2. Check `journalctl` for:

   * USB disconnects
   * undervoltage warnings
   * camera crashes
3. Check monitor logs for:

   * ping failures
   * high temperatures
   * throttling flags
4. Compare timestamps between logs

---

# Helpful Commands Summary

| Action                  | Command                            |
| ----------------------- | ---------------------------------- |
| Live front camera logs  | `journalctl -u ustreamer_front -f` |
| Previous boot logs      | `journalctl -b -1`                 |
| Kernel/USB logs         | `journalctl -k`                    |
| Monitor log folder      | `ls /home/pi/rov_logs`             |
| Follow monitor log live | `tail -f <logfile>`                |
| Exit viewer             | `q`                                |

---

# Important Notes

* Logs are automatically timestamped
* Logs persist across reboots
* Old logs are extremely valuable for diagnosing intermittent problems
* Do not delete logs unless storage space becomes an issue
