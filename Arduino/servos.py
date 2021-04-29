import math
import tkinter as tk
from time import sleep,time
import serial

class Servo:
	start = 0.0
	(bpm, amp, min, duty, func) = (30,100,0,0,"|sin|")
	data = []
	time = []

	def __init__(self,addr):
		# Initialize the Serial Communication with te Arduino
		self.addr = addr
		self.ser = ser = serial.Serial(port=addr, baudrate=115200, timeout=0.1)

		ser.flushInput()
		ser.flushOutput()
		sleep(2)


		self.func = self.switch(self.func)

	def reset(self):
		# Slowly Lower the Duty Cycle
		if (self.duty > self.min):
			while (self.duty > self.min):
				self.writeDuty(self.duty)
				self.duty -= 1
				sleep(0.01)
		else:
			while (self.duty < self.min):
				self.writeDuty(self.duty)
				self.duty += 1
				sleep(0.01)

		# Reinitialize Values
		self.start = time()
		self.data = []
		self.time = []

	def update(self):
		t = time() - self.start
		self.func(t)
		self.fillArr(self.duty,t)
		self.writeDuty(self.duty)

	# These are the Availible Functions
	def squared(self,t):
		self.duty = (self.amp-self.min)*math.pow(math.sin((self.bpm/120.0)*((t)*2.0*math.pi)),2)+self.min
	def fourth(self,t):
		self.duty = (self.amp-self.min)*math.pow(math.sin((self.bpm/120.0)*((t)*2.0*math.pi)),4)+self.min
	def sixth(self,t):
		self.duty = (self.amp-self.min)*math.pow(math.sin((self.bpm/120.0)*((t)*2.0*math.pi)),6)+self.min
	def absolute(self,t):
		self.duty = (self.amp-self.min)*abs(math.sin((self.bpm/120.0)*((t)*2.0*math.pi)))+self.min

	def fillArr(self,point,time):
		# This fills the data array to be used when plotting
		self.data.append(point)
		self.data = self.data[-100:]

		self.time.append(time)
		self.time = self.time[-100:]

	def writeDuty(self,val):
		# Reformat the
		temp = str(math.floor(val)).encode()
		#print(temp)
		# self.ser.flushOutput()
		#sleep(0.1)
		self.ser.write(temp)
		# print("Written",self.duty)

	def switch(self,arg):
		# Switch Case for the function
		switcher = { "|sin|":self.absolute,"sin^2":self.squared,
			"sin^4":self.fourth,"sin^6":self.sixth}
		return switcher.get(arg,"invalid")

	def _close(self):
		self.ser.close()

if __name__ == "__main__":

	servos = Servo("/dev/cu.usbserial-14130")

	while(1):
		servos.update()
		#temp = servos.ser.readline()

		#print(temp)
		sleep(0.1)
