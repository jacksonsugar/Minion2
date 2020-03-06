#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import os
import configparser

i = 0
light = 12
wifi = 22
Press_IO = 29

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(light, GPIO.OUT)
GPIO.setup(wifi, GPIO.OUT)
GPIO.setup(Press_IO, GPIO.OUT)
GPIO.output(Press_IO, 1)
GPIO.output(wifi, 1)

config = configparser.ConfigParser()
config.read('/home/pi/Desktop/Minion_config.ini')

Ddays = int(config['Deployment_Time']['days'])
Dhours = int(config['Deployment_Time']['hours'])
Srate = float(config['Sample_Rate']['minion_sample_rate'])
Isample = float(config['Initial_Samples']['hours'])

TotalSamples = (((Ddays*24)+Dhours)-Isample)/Srate

print(TotalSamples)

####################################
Samples = TotalSamples
####################################

ifswitch = "sudo python /home/pi/Documents/Minion_tools/dhcp-switch.py"

iwlist = 'sudo iwlist wlan0 scan | grep "Minion_Hub"'

net_cfg = "ls /etc/ | grep dhcp"

ping_hub = "ping 192.168.0.1 -c 1"

ping_google = "ping google.com -c 1"

subpkill = "sudo killall python"

def flash():
        j = 0
        while j <= 2:
                GPIO.output(light, 1)
                time.sleep(.25)
                GPIO.output(light, 0)
                time.sleep(.25)
                j = j + 1

def off():
	GPIO.output(light, 0)

def on():
	GPIO.output(light, 1)


if __name__ == '__main__':

	if len(os.listdir('/home/pi/Documents/minion_pics') ) == 0:
		os.system('sudo python3 /home/pi/Documents/Minion_scripts/Init_T+P.py')


	if len(os.listdir('/home/pi/Documents/minion_pics')) == Samples:
        GPIO.output(Press_IO, 0)
	
	if len(os.listdir('/home/pi/Documents/minion_pics')) == Samples + 1:
		os.system('sudo python3 /home/pi/Documents/Minion_scripts/Final_T+P.py')

	os.system('sudo python /home/pi/Documents/Minion_scripts/Temp+Pres.py &')
	os.system('sudo python /home/pi/Documents/Minion_scripts/Minion_image.py')

	## Check for wifi

	wifi_status = os.popen(iwlist).read()

	if "Minion_Hub" in wifi_status:
		print("WIFI!!")
		status = "Connected"
		net_status = os.popen(net_cfg).read()
		if ".minion" in net_status:
			os.system(ifswitch)
		else:
			print("You have Minions!")

	else:
		print("No WIFI found.")
		status = "Not Connected"

	print(status)

	if status == "Connected":
		flash()
		os.system(subpkill)
		exit(1)
	else:
		print('Goodbye')
		GPIO.output(wifi, 0)
		time.sleep(5)
		os.system('sudo shutdown now')
