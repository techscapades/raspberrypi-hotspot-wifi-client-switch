A simple script which uses a momentary push button connection between
ground and a user definable gpio pin to toggle between wifi client and
wifi hotspot mode, it uses a config file which contains the SSIDs and
passphrases of the 2 networks. It allows you to change config parameters, run scripts etc..
on the raspberrypi through ssh using hotspot without the need for a router
and then once done you can change it back to a normal wifi network

Modes: 
1 = wifi client mode - connects you to a wifi router 
2 = wifi hotspot mode - your raspberrypi acts as a "router"
Change the default mode in the config file.

I use network manager to do this, running well on my raspberry pi
zero w 2 on raspbian bookworm. 

There are 2 versions of the code, the basic version which will 
work out the box is the one without the SSD1306 suffix. However to 
use the version with SSD1306 you gotta follow these instructions
and install adafruit circuit python on the raspberrypi:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/circuitpython-raspi
then after activating the virtual environment follow these steps to use the SSD1306:
https://learn.adafruit.com/monochrome-oled-breakouts/python-setup

if you intend to use the SSD1306 version and want to run the programme at startup , 
I used ~/.bashrc to start the virtual environment, 
and to start the programme I used systemd, steps to follow, replace $USER with your username:
1. create a bash script

<code>/home/$%USER/startcircuitpythonenv.sh</code>

2. copy the following into the file and save

<code>#!/bin/sh
source /home/rpz21/env/bin/activate
echo started circuitpython environment
</code>

3. sudo nano ~/.bashrc and append this into the end of the file

<code>if [ -f ~/startcircuitpythonenv.sh ]; then
        . ~/startcircuitpythonenv.sh
fi
</code>

4. create a bash script to run the toggle_HS_client_SSD1306.py code called runoled.sh and past this into it:

<code>#!/bin/bash
sudo /home/$USER/env/bin/python /home/$USER/toggle_HS_client_SSD1306.py
</code>

5.  create a systemd service to run this code

<code>sudo nano /etc/systemd/system/startoled.service</code>

6. past this into the service and save

<code>[Unit]
Description=begin HS <=> wifi client serivce

[Service]
Type=simple
ExecStart=/usr/bin/bash /home/$USER/runoled.sh
Restart=always

[Install]
WantedBy=multi-user.target</code>

7. <code>sudo systemctl enable startoled.service</code>
8. <code>sudo systemctl daemon-reload</code>
9. <code>sudo systemctl start startoled.service to check that its working</code>

If you want to use the power and oled saving mode use "toggle_HS_client_SSD1306_power_save.py", this
will turn the display off after 20 seconds, press once to wake the display, pressing again will toggle 
the modes. I recommend using this version because it preserves the OLED from burn in

All the best :)
