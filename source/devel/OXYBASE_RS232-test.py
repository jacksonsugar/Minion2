import time
import serial

reply = ''

ser= serial.Serial(
	port='/dev/ttyUSB0', #serial port the object should read
	baudrate= 19200,      #rate at which information is transfered over comm channel
	parity=serial.PARITY_NONE, #no parity checking
	stopbits=serial.STOPBITS_ONE, #pattern of bits to expect which indicates the end of a character
	bytesize=serial.EIGHTBITS, #number of data bits
	timeout=1
)

time.sleep(1)

print('Welcome to the OXYBASE tester v0.1')
print('Please type your commands below:')

while(1):

	cmd = raw_input('-> ')

	cmd = cmd + '\r'

	ser.write(cmd)

	reply = ser.read_until('\r\r')

	print(reply)
