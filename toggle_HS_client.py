'''
This sketch uses a momentary push button to toggle between hotspot and wifi client modes
based on a user defined config file which holds the config for the wifi hotspot and wifi
client networks, potential future improvements would be to include visual feedback from
LEDs or from a small OLED display, have fun :)
-techscapades
'''

'''==========================================SETUP=========================================='''
# define time variables
import time
connection_sleep_time = 10
poll_time = 1
error_to_exit_time = 60

# try to read the from path/to/config_file.txt and populate command f-strings
config_filename = 'toggle_HS_client_config.txt'
config = {}
try:
	with open(config_filename, 'r') as file:
		lines = file.readlines()
	for line in lines:
		line = line.strip()
		if line:
			key, value = line.split('=',1)
			config[key.strip()] = value.strip()
	hotspot_SSID = config.get('hotspot_SSID')
	hotspot_PW = config.get('hotspot_PW')
	start_hs_cmd = f"sudo nmcli d wifi hotspot ifname wlan0 ssid {hotspot_SSID} password {hotspot_PW}"
	wifi_SSID = config.get('wifi_SSID')
	wifi_PW = config.get('wifi_PW')
	stop_hs_start_wifi_cmd = f"sudo nmcli con down id {hotspot_SSID} && sudo nmcli d wifi connect {wifi_SSID} password {wifi_PW}"
	start_wifi_cmd = f"sudo nmcli d wifi connect {wifi_SSID} password {wifi_PW}"
	default_mode = config.get('default_mode')
	button_pin = config.get('button_pin')
	config_read_success = True
except:
	print(f'config file: {config_filename} not found, exiting in 60 seconds')
	config_read_success = False
	time.sleep(error_to_exit_time)

# import Button class from gpiozero and define pin to attach button to
from gpiozero import Button
button_pin = int(button_pin) # following gpio definition
button = Button(button_pin)
# optional booleans for complex control
switched_modes = True
button_pressed = False

# get the current ip address and determine which mode system is currently in
import socket
import os
def get_ip_address(interface):
	try:
        	# Get the IP address associated with the given interface
        	ip_address = os.popen(f'ip addr show {interface}').read().split("inet ")[1].split("/")[0]
        	return ip_address
	except IndexError:
	        return None

interface = 'wlan0'
ip_address = get_ip_address(interface)

def check_if_hs_active(ip_address):
	# use the return value in LOOP
	if ip_address == '10.42.0.1' or ip_address =='10.42.0.255':
		return True
	else:
		return False

# set the system into user defined default state from config file
import subprocess
# *********** modes are defined as: 1 for wifi, 2 for hotspot ************
if ip_address == '10.42.0.1' or ip_address =='10.42.0.255':
	# change the 10.x.x.x to whatever your hotspot IP is, use 'ifconfig' command in terminal to find out
        current_mode = 2
else:
        current_mode = 1
default_mode = int(default_mode)
print(f"default mode: {default_mode}")
print(f"current mode: {current_mode}")
if current_mode != default_mode:
	if current_mode == 1:
		print('setting current mode from 1 to 2')
		process = subprocess.Popen(start_hs_cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
	elif current_mode == 2:
		print('setting current mode from 2 to 1')
		process = subprocess.Popen(stop_hs_start_wifi_cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
	time.sleep(connection_sleep_time)
if check_if_hs_active(get_ip_address(interface)):
        current_mode = 2
else:
        current_mode = 1
print(f"current mode: {current_mode}")


'''==========================================LOOP=========================================='''
print(f'Polling button pin: gpio-{button_pin}')
while True:
	if button.is_pressed:
		switched_modes = False
		button_pressed = True
	if not switched_modes and button_pressed:
		# this if statement isn't necessary but I included it for my own control
		print("toggling modes")
		# toggle the modes from wifi client to hotspot
		if current_mode == 1:
			process = subprocess.Popen(start_hs_cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
		else:
			process = subprocess.Popen(stop_hs_start_wifi_cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
		# give some debounce for the button
		time.sleep(connection_sleep_time)
		# check what the current mode it
		if check_if_hs_active(get_ip_address(interface)):
        		current_mode = 2
		else:
        		current_mode = 1
		print(f"current mode: {current_mode}")
		# reset variables
		switched_modes = True
		button_pressed = False
	# change this to reduce the reactiveness
	time.sleep(poll_time)
