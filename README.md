A simple script which uses a momentary push button connection between
ground and a user definable gpio pin to toggle between wifi client and
wifi hotspot mode, it uses a config file which contains the SSIDs and
passphrases of the 2 networks. 

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

All the best :)
