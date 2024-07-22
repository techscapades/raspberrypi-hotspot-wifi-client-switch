A simple script which uses a momentary push button connection between
ground and a user definable gpio pin to toggle between wifi client and
wifi hotspot mode, it uses a config file which contains the SSIDs and
passphrases of the 2 networks. 

Modes: 
1 = wifi client mode - connects you to a wifi router 
2 = wifi hotspot mode - your raspberrypi acts as a "router"
Change the default mode in the config file.

I use network manager to do this, running well on my raspberry pi
zero w 2 on raspbian bookworm. I intend to add an oled display or neopixel
to the circuit to show the different modes visually
