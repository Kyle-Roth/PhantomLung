import tkinter as tk
import math
import RPi.GPIO as GPIO
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt

class servofunctions:
	start = 0.0 #time variable used for step size
	freq = 0 #frequency in BPM
	A = 0 #amplitude of functions
	M = 21 #offset of functions
	t = 21 #range 21 to 98 (roughly 30mm)
	error = False #for checking if error in user inputs
	data = []
	time = []
	#GPIO initialization for PWM signal
	pin = 33
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin,GPIO.OUT)
	pin_pwm = GPIO.PWM(pin,450) #450 Hz
	pin_pwm.start(21) #start at location 0
	pin_pwm.ChangeDutyCycle(21)

	def reset(self): #resets the robot to the current offset - called when updating, pausing, or closing program (closing window)
		if (self.t > self.M): #branch moves phantom lung back to offset
			while (self.t > self.M):
				self.t -= 1
				self.pin_pwm.ChangeDutyCycle(self.t)
				sleep(0.01)
		else: #branch moves phantom lung forward to offset
			while (self.t < self.M):
				self.t += 1
				self.pin_pwm.ChangeDutyCycle(self.t)
				sleep(0.01)
		self.start = time() #resets step to zero - equivalent to resetting iteration
		
		# Clear Data
		#self.data = []
		#self.time = []
	def checkduty(self,amp,off): #keeps duty cycle within proper value range and keeps program from crashing when invalid inputs are given
		if((amp+off)>98.0):
			if(not self.error): #makes message only print once when error occurs until it is fixed then occurs again
				print("ERROR: Amp + Offset must be less than 101\n Please update to proper parameters and process will continue") #error message
			self.reset() #pauses at current offset until valid inputs are read in
			self.error = True
			return False
		else:
			if(self.error):
				print("Back to work") #lets user know the process should be running properly again
				self.error = False
			return True
		
	def squared(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)),2)+self.M
		if(self.checkduty(self.A,self.M)):
			self.pin_pwm.ChangeDutyCycle(self.t)
		#self.fillArr(self.t,time()-self.start)
				
	def fourth(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)),4)+self.M
		if(self.checkduty(self.A,self.M)):
			self.pin_pwm.ChangeDutyCycle(self.t)
		#self.fillArr(self.t,time()-self.start)
				
	def sixth(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)),6)+self.M
		if(self.checkduty(self.A,self.M)):
			self.pin_pwm.ChangeDutyCycle(self.t)
		#self.fillArr(self.t,time()-self.start)
				
	def absolute(self):
		self.t = self.A*abs(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)))+self.M
		if(self.checkduty(self.A,self.M)):
			self.pin_pwm.ChangeDutyCycle(self.t)
		#self.fillArr(self.t,time()-self.start)
		
	#def fillArr(self,point,time):
	#	self.data.append((point-21)/.77)
	#	self.data = self.data[-100:]
	#	
	#	self.time.append(time)
	#	self.time = self.time[-100:]
