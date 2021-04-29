import tkinter as tk
import math
import RPi.GPIO as GPIO
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt

class servofunctions:
	start = 0.0
	freq = 0
	A = 0
	M = 21
	t = 21
	data = []
	time = []
	start =0
	
	#range 21 to 98 (roughly 30mm)
	power = 0
	powerfunc = 1
	pin = 33
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin,GPIO.OUT)
	pin_pwm = GPIO.PWM(pin,450)
	pin_pwm.start(21)
	pin_pwm.ChangeDutyCycle(21)

	def reset(self):
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
		self.start = time()
		
		# Clear Data
		self.data = []
		self.time = []
	
	def squared(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)),2)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		self.fillArr(self.t,time()-self.start)
				
	def fourth(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)),4)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		self.fillArr(self.t,time()-self.start)
				
	def sixth(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)),6)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		self.fillArr(self.t,time()-self.start)
				
	def absolute(self):
		self.t = self.A*abs(math.sin((self.freq/120.0)*((time()-self.start)*2.0*math.pi)))+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		self.fillArr(self.t,time()-self.start)
		
	def fillArr(self,point,time):
		self.data.append((point-21)/.77)
		self.data = self.data[-100:]
		
		self.time.append(time)
		self.time = self.time[-100:]
