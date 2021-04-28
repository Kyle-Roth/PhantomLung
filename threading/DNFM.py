import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame
from time import sleep
from TeraRanger_Evo_UART import TeraRanger
import math
import RPi.GPIO as GPIO
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

# Custom Libraries
from GUI import MainWindow
from servos import Servos
from TeraRanger_Evo_UART import TeraRanger

class Data:
	
	def __init__(self):
		self.length = 5000
		
		self.sTime = []
		self.sData = []
		
		self.eTime = []
		self.sData = []

	def getS(self):
		return sTime,sData
		
	def addS(self,time,data):
		# append the new data points and strip the oldest point
		self.sTime.append(time)
		self.sTime = self.sTime[-self.length:]
		
		self.sData.append(data)
		self.sData = self.sData[-self.length:]
	
	def getE(self):
		return eTime,eData
		
	def addE(self,time,data):
		# append the new data points and strip the oldest point
		self.eTime.append(time)
		self.eTime = self.eTime[-self.length:]
		
		self.eData.append(data)
		self.eData = self.eData[-self.length:]

if __name__=='__main__':
	
	
	# Set up manager for sharing data between processes
	BaseManager.register("pltData",Data)
	m = BaseManager()
	m.start()
	data = m.pltData(0)
	
	servo = Servos()
	#evo = TeraRanger()
	
	root = tk.Tk()
	Window = MainWindow(root)


	#evo.start()
	
	#while(1):
	#	continue
		#print(evo.data,evo.time)
		#print(servo.data)
		
	# Main Loop
	while(root):
		if Window.UpdateCheck:
			if Window.running:
				# Pass Data to the Servo
				servo.newVals = [Window.OFF, Window.AMP, Window.BPM, Window.FUNC]
				servo.updateCheck = 1
				servo.running = 1
				
				#evo.updateCheck = 1
				#evo.running = 1
				
				Window.UpdateCheck = 0
			else:
				# Pass Data to the Servo
				servo.newVals = [21, 0, 0, Window.FUNC] #21 duty cycle corresponds with 0 location
				servo.updateCheck = 1
				servo.running = 0

				#evo.updateCheck = 1
				#evo.running = 0
							
				Window.UpdateCheck = 0
				
		elif(Window.running==1):
			Window.updatePlot(servo.time,servo.data)
			
		if Window.ExitFlag == False:
			root.update()
		else:
			break
		
	
	print("Here")
	servo.join()
	#evo.join()
