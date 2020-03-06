# Written to make switching wireless networks easier!
# Be careful, as you need to be in .minion in order to retain your static IP

# Here we will ensure the Minion is using its local IP once it is connected to the Hub

# import needed libraries for scanning and executing
import glob, os
import time

# Iterator
i = 0

# User defined loop for style points
def plz_wait():
	for i in range(0,3):
		print "_____________________"
		time.sleep(1)
		i = i + 1

# Filenames of interest
minion = "dhcpcd.minion"
internet = "dhcpcd.internet"
# Target Directory
os.chdir("/etc")
# List of dhcpcd.* files
files = []
# Scan for files
for file in glob.glob("dhcpcd.*"):
	files.append(file)

#If you wanna see the output
#print files

# Decide what to do with this information

# Copy the .conf to the missing file and move the alt to .conf

if minion in files:
	os.system('sudo cp /etc/dhcpcd.conf /etc/dhcpcd.internet')
	print "Copying .conf to .internet"
	os.system('sudo cp /etc/dhcpcd.minion /etc/dhcpcd.conf')
	print "Copying .minion to .conf"
	os.system('sudo rm -rf /etc/dhcpcd.minion')
	print "Now you have Minion_Hub!"

elif internet in files:
	print "You are alread on the Minion Network!"


# Cheaky response when things are bad
else:
	print "Bro you messed it up..."

# Restart network interfaces for actions to take effect
os.system('sudo service dhcpcd restart')

print "Done!"

# yay.
