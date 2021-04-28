

import math
import RPi.GPIO as GPIO
from time import sleep,time


class Servos:
	#variables that are needed to do things
	startTime = 0
	freq = 0 #frequency in BPM
	A = 0 #amplitude
	M = 21 #minimum
	t = 21 #range 21 to 98 (roughly 30mm)
	data = []
	time = []
	#pin and GPIO initialization
	pin = 33
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin,GPIO.OUT)
	pin_pwm = GPIO.PWM(pin,450)
	#initialzes location to 0
	pin_pwm.start(21)
	pin_pwm.ChangeDutyCycle(21)
	
	# Status Variables
	running = 0
	updateCheck = 0
	newVals = ["Off","Amp","BPM","Func"]
	
	def __init__(self):
		self.func = self.absolute
		self.reset()
		
	def run(self,sharedData):
		while 1: # Window was updated
			if self.updateCheck:
				if self.running:
					self.M = self.newVals[0]
					self.A = self.newVals[1]
					self.freq = self.newVals[2]
					self.func = self.switch(self.newVals[3])
					self.reset()
					self.updateCheck = 0
				else:
					self.M = 21
					self.reset()
					self.updateCheck = 0
			elif self.running:
				data,tim = self.func()
				sharedData.addS(time,data)
				
	def reset(self): #sets robot to the set minimum before continuing calculations
		if (self.t > self.M):	
			while (self.t > self.M):
				self.t -= 1
				self.pin_pwm.ChangeDutyCycle(self.t)
				sleep(0.01)
		else:
			while (self.t < self.M):
				self.t += 1
				self.pin_pwm.ChangeDutyCycle(self.t)
				sleep(0.01)
		self.startTime = time() #restarts timer
		
		#clear data for plot
		self.data = []
		self.time = []
	
	def switch(self,arg):
		switcher = { "|sin|":self.absolute,"sin^2":self.squared,
			"sin^4":self.fourth,"sin^6":self.sixth}
		return switcher.get(arg,"invalid")
	
	
	def squared(self): #calculation for sine squared movement pattern
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)),2)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t) #moves servos to move robot
		return (self.t,time()-self.startTime) #puts data into array for plotting
				
	def fourth(self): #calculation for sine quarticed movement pattern
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)),4)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		return (self.t,time()-self.startTime)
				
	def sixth(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)),6)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		return (self.t,time()-self.startTime)
				
	def absolute(self):
		self.t = self.A*abs(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)))+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		return (self.t,time()-self.startTime)

	def fillArr(self,point,time):
		self.data.append((point-21)/.77)
		self.data = self.data[-10000:]
		
		self.time.append(time)
		self.time = self.time[-10000:]
