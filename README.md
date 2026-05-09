# ROVUtils

This repo contains a few things:
- autostart for the camera stream (ustreamer)
- logging stuff


## Autostart

### Configuration
There a few key details about the autostart process. 

1. Make sure the absolute path to ustreamer is correct (spelling, capitalization,etc).
2. Check the camera paths (which video device), ports, resolutions, etc are correct. 

### Setup

1. Move the respective camera service file into: /etc/systemd/system/
    i. You can either use copy / paste with GUI, or you can use the cp command:
    ii. Ex. `cp /home/mamorobotics/front_camera.service /etc/systemd/system/`
2. Run: `sudo systemctl daemon-reload`
3. Run: "sudo systemctl enable [name of service]"
    i. Ex. `sudo systemctl enable front_camera` or `sudo systemctl enable lower_camera`
4. The, run: "sudo systemctl start [name of service]"
    i. Ex. `sudo systemctl start front_camera` or `sudo systemctl start lower_camera`
5. You should be good! You need to re-do these steps every time you change the service file. 



## Logging

### Custom Logs

#### Setup
1. Clone the repo. 
2. Install the requirements by running `pip install psutil`. 
3. Make sure when you run: `vcgencmd`, it works (and has a valid output). If it says command not found, then run `sudo apt install libraspberrypi-bin`. 
3. Make sure the paths in the `rov_logger.service` are correct. For Python, the monitor.py file, and the logging folder path. 
4. Start the service using the process for autostart above. 



### System / Ustreamer logs

#### Setup
1. Most of it is automatically configured through either default Pi / linux settings, or through the autostart in the front / lower camera service files. 
2. Check that persistent logging is setup, run: `ls /var/log/journal`
    i. If the folder is empty, it means that persistent logging is not setup. 
3. If needed, setup persistent logging: 
```
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
```

#### Usage
There are two types of logs: system / ustreamer logs, accessed through journalctl, and the custom logs we setup using the Python code in this repo. The former logs, can be accessed through journalctl, the latter can be access through the files (should be in /home/mamorobotics/rov_logs or something like that). The path can be found in the source code. 

A helpful guide on how to parse through and understand these logs is found in LOGS_GUIDE.md

## Todo

### Autostart

### Loggging:
