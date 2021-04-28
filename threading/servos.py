
import math
import RPi.GPIO as GPIO
from time import sleep,time

class ServoData:
	def __init__(self,trash=None):
		self.freq = 15
		self.amp = 77
		self.min = 21
		self.data = []
		self.time = []
		self.func = "|sin|"
		self.running = 1		# CHANGE LATER RUNS AT STARTUP
		self.update = 1 
		
	def getAll(self):
		return self.freq,self.amp,self.min,self.func
	
	def setAll(self,f,a,m,d):
		self.freq = f
		self.amp = a
		self.min = m
		self.duty = d
		
	def getData(self):
		return self.time,self.data
	
	def addData(self,tim,dat):
		# append the new data points and strip the oldest point
		self.time.append(tim)
		self.time = self.time[-5000:]
		
		self.data.append(dat)
		self.data = self.data[-5000:]
	
	def setStatus(self,run,up):
		self.running = run
		self.update = up

	def getStatus(self):
		return self.running,self.update

	def reset(self):
		self.data = []
		self.time = []


	
class Servos:


	
	def __init__(self,sData):
		
		#variables that are needed to do things
		self.startTime = 0
		self.freq = 0 #frequency in BPM
		self.A = 0 #amplitude
		self.M = 21 #minimum
		self.t = 21 #range 21 to 98 (roughly 30mm)
		
		self.func = self.absolute
		
		#pin and GPIO initialization
		pin = 33
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin,GPIO.OUT)
		self.pin_pwm = GPIO.PWM(pin,450)
		#initialzes location to 0
		self.pin_pwm.start(21)
		self.pin_pwm.ChangeDutyCycle(30)

		self.reset()
		self.run(sData)
		
	def run(self,sharedData):
		while 1: # Window was updated
			# get program status
			running, update = sharedData.getStatus()
			
			if update:
				if running:
					self.freq,self.A,self.M,self.func = sharedData.getAll()
					self.func = self.switch(self.func)
					self.reset()
					sharedData.reset()
					sharedData.setStatus(1,0)
					
				else:
					self.M = 21
					self.reset()
					sharedData.reset()
					sharedData.setStaus(0,0)
					
			elif running:
				tim,dat = self.func()
				sharedData.addData(tim,dat)

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
	
	def switch(self,arg):
		switcher = { "|sin|":self.absolute,"sin^2":self.squared,
			"sin^4":self.fourth,"sin^6":self.sixth}
		return switcher.get(arg,"invalid")
	
	
	def squared(self): #calculation for sine squared movement pattern
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)),2)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t) #moves servos to move robot
		
		return (time()-self.startTime,self.t)
				
	def fourth(self): #calculation for sine quarticed movement pattern
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)),4)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)

		return (time()-self.startTime,self.t)
						
	def sixth(self):
		self.t = self.A*math.pow(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)),6)+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		
		return (time()-self.startTime,self.t)
				
	def absolute(self):
		self.t = self.A*abs(math.sin((self.freq/120.0)*((time()-self.startTime)*2.0*math.pi)))+self.M
		self.pin_pwm.ChangeDutyCycle(self.t)
		
		return (time()-self.startTime,self.t)
		
	def fillArr(self,point,time):
		self.data.append((point-21)/.77)
		self.data = self.data[-10000:]
		
		self.time.append(time)
		self.time = self.time[-10000:]
