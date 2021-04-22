import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame
from time import sleep
from TeraRanger_Evo_UART import TeraRanger
import math
import RPi.GPIO as GPIO
from time import sleep,time
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

# Custom Libraries
from GUI import MainWindow
from servos import servofunctions
from TeraRanger_Evo_UART import TeraRanger

def switch(arg):
	switcher = { "|sin|":servo.absolute,"sin^2":servo.squared,
		"sin^4":servo.fourth,"sin^6":servo.sixth}
	return switcher.get(arg,"invalid")


if __name__=='__main__':
	servo = servofunctions()
	evo = TeraRanger()
	func = servo.absolute
	root = tk.Tk()
	Window = MainWindow(root)

	eData = []
	eTime = []
	t = Thread(target = evo.streamData,args = (eData,eTime))
	t.start()
	
	# Main Loop
	while(1):
		if(Window.UpdateCheck==1):
			if Window.running:
				servo.A = Window.AMP
				servo.M = Window.OFF
				servo.freq = Window.BPM
				func = switch(Window.FUNC)
				servo.reset()
				evo.reset()
				Window.UpdateCheck = 0
			else:
				servo.M = 21 #21 duty cycle corresponds with 0 location
				servo.reset()
				evo.reset()
				Window.UpdateCheck = 0
				
		elif(Window.running==1):
			func()
			print(eData,eTime)
			Window.updatePlot(servo.time,servo.data,eTime,eData)
			
		root.update()
