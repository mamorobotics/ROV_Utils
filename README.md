# ROVUtils

This repo contains a few things:
- autostart for the camera stream (ustreamer)
- logging stuff


## Autostart

### Configuration

### Setup

1. Move the respective camera service file into: /etc/systemd/system/
2. Run: `sudo systemctl daemon-reload`
3. Run: "sudo systemctl enable [name of service]"
    i. Ex. `sudo systemctl enable front_camera` or `sudo systemctl enable lower_camera`
4. The, run: "sudo systemctl start [name of service]"
    i. Ex. `sudo systemctl start front_camera` or `sudo systemctl start lower_camera`
5. You should be good!



## Logging

### Custom Logs

#### Setup
1. Clone the repo. 
2. Install the requirements by running `pip install psutil`. 
3. Make sure when you run: `vcgencmd`, it works (and has a valid output). If it says command not found, then run `sudo apt install libraspberrypi-bin`. 
3. Make sure the paths in the `rov_logger.service` are correct.
4. Start the service using the process for autostart above. 


### Reading System / UStreamer logs


## Todo

### Autostart

### Loggging:
- [ ] Check original requirements
- [ ] check persistent logging
- [ ] Write guide for examining logs (journald)
