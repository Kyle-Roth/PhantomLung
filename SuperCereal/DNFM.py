import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame
from time import sleep
import math
import RPi.GPIO as GPIO
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt

# Custom Libraries
from GUI import MainWindow
from servos import servofunctions
#from TeraRanger_Evo_UART import TeraRanger

def switch(arg): #equivalent of switch case in python. dictionary look up/jump table
	switcher = { "|sin|":servo.absolute,"sin^2":servo.squared,
		"sin^4":servo.fourth,"sin^6":servo.sixth}
	return switcher.get(arg,"invalid")

if __name__=='__main__':
	servo = servofunctions() #creates object to control robot
	func = servo.absolute #initializes breathing pattern
	root = tk.Tk() #creates window for tkinter
	Window = MainWindow(root) #creates object to control tkinter


	# Main Loop
	while(1): 
		if(Window.UpdateCheck==1): #runs if update or start/stop has been clicked in GUI (or if exiting)
			if Window.running:
				servo.A = Window.AMP #these all take GUI values and sends them to the pattern calculations in servo
				servo.M = Window.OFF
				servo.freq = Window.BPM
				func = switch(Window.FUNC)
				servo.reset() #resets the robot to the offset
				Window.UpdateCheck = 0 #stops this branch from running multiple times without user input
			else: #resets the robot to zero position when stopped or exiting
				servo.M = 21 #21 duty cycle corresponds with 0 location
				servo.reset()
				Window.UpdateCheck = 0
				
		elif(Window.running==1):
			func() #runs selected function in servofunctions to move the robot
			#Window.updatePlot(servo.time,servo.data) #updates plot
		
		root.update() #checks GUI for input
	
