import tkinter as tk
import math
import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import matplotlib.pyplot as p


freq = 0
i = 0
m = 1
A = 77
M = 21
t = 21
#range 21 to 98 (roughly 28.5mm)
power = 0
powerfunc = 1
pin = 33
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)
pin_pwm = GPIO.PWM(pin,450)
pin_pwm.start(21)
pin_pwm.ChangeDutyCycle(21)
root = tk.Tk()

def exit():
	reset()
	root.destroy()
root.protocol("WM_DELETE_WINDOW",exit)

def reset():
	global M
	global t
	global i
	i = 0
	if (t > M):	
		while (t > M):
			t -= 1
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.01)
	else:
		while (t < M):
			t += 1
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.01)

def handle_button(event):
	global freq
	freq = s.get()
	reset()

button = tk.Button(root,text="Update BPM",width=15,height=5,bg="blue",fg="white")
button.bind("<Button-1>",handle_button)
button.grid(column=0,row=1)

def handle_buttona(event):
	global A
	A = (sa.get())*0.77
	reset()

buttona = tk.Button(root,text="Update Amplitude",width=15,height=5,bg="blue",fg="white")
buttona.bind("<Button-1>",handle_buttona)
buttona.grid(column=1,row=1)

def handle_buttonm(event):
	global M
	M = (sm.get())*0.77 + 21
	reset()

buttonm = tk.Button(root,text="Update Minimum",width=15,height=5,bg="blue",fg="white")
buttonm.bind("<Button-1>",handle_buttonm)
buttonm.grid(column=2,row=1)

def change_mode(event):
	global m
	if (m==1):
		m = 0
		mode_button.config(text="Mode = Default")
	else:
		m = 1
		mode_button.config(text="Mode = Custom")
mode_button = tk.Button(root,text="Mode = Custom",width=15,height=5,bg="blue",fg="white")
mode_button.bind("<Button-1>",change_mode)
mode_button.grid(column=3,row=1)

def squared(event):
	global power
	power = 2
	global i
	global m
	global t
	global freq
	global A
	global M
	global powerfunc
	powerfunc = 1
	reset()
	while(1):
		if (m == 0):
			i += 1
			t = 77*math.pow(math.sin(0.125*(i*2.0*math.pi/1000.0)),2)+21
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)	
			if (i%10 == 0):
				#print(freq)
				root.update()
		if (m == 1):
			i += 1
			t = A*math.pow(math.sin((freq/120.0)*(i*2.0*math.pi/1000.0)),2)+M
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)
			if (i%10 == 0):
				#print(t)
				root.update()
sqbutton = tk.Button(root,text="Run Squared",width=10,height=5,bg="blue",fg="white")
sqbutton.bind("<Button-1>",squared)
sqbutton.grid(column=0,row=0)

def fourth(event):
	global power
	power = 4
	global i
	global m
	global t
	global freq
	global A
	global M
	global powerfunc
	powerfunc = 1
	reset()
	while(1):
		if (m == 0):
			i += 1
			t = 77*math.pow(math.sin(0.125*(i*2.0*math.pi/1000.0)),4)+21
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)	
			if (i%10 == 0):
				#print(freq)
				root.update()
		if (m == 1):
			i += 1
			t = A*math.pow(math.sin((freq/120.0)*(i*2.0*math.pi/1000.0)),4)+M
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)
			if (i%10 == 0):
				#print(t)
				root.update()
fobutton = tk.Button(root,text="Run Fourth",width=10,height=5,bg="blue",fg="white")
fobutton.bind("<Button-1>",fourth)
fobutton.grid(column=1,row=0)

def sixth(event):
	global power
	power = 6
	global i
	global m
	global t
	global freq
	global A
	global M
	global powerfunc
	powerfunc = 1
	reset()
	while(1):
		if (m == 0):
			i += 1
			t = 77*math.pow(math.sin(0.125*(i*2.0*math.pi/1000.0)),6)+21
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)	
			if (i%10 == 0):
				#print(freq)
				root.update()
		if (m == 1):
			i += 1
			t = A*math.pow(math.sin((freq/120.0)*(i*2.0*math.pi/1000.0)),6)+M
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)
			if (i%10 == 0):
				#print(t)
				root.update()
sibutton = tk.Button(root,text="Run Sixth",width=10,height=5,bg="blue",fg="white")
sibutton.bind("<Button-1>",sixth)
sibutton.grid(column=2,row=0)

def absolute(event):
	global i
	global m
	global t
	global freq
	global A
	global M
	global powerfunc
	powerfunc = 0
	reset()
	while(1):
		if (m == 0):
			i += 1
			t = 77*abs(math.sin(0.125*(i*2.0*math.pi/1000.0)))+21
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)	
			if (i%10 == 0):
				#print(freq)
				root.update()
		if (m == 1):
			i += 1
			t = A*abs(math.sin((freq/120.0)*(i*2.0*math.pi/1000.0)))+M
			pin_pwm.ChangeDutyCycle(t)
			sleep(0.001)
			if (i%10 == 0):
				#print(t)
				root.update()
abbutton = tk.Button(root,text="Run Absolute",width=10,height=5,bg="blue",fg="white")
abbutton.bind("<Button-1>",absolute)
abbutton.grid(column=3,row=0)

def plot():
	p.clf()
	global freq
	global M
	global A
	global power
	global powerfunc
	global absfunc
	x = np.arange(0,100,0.1)
	if(powerfunc==1):
		y = A*np.power(np.sin(freq*(x*2.0*math.pi/1000.0)),power)+M
		p.plot(x,y)
		p.title('Sine^power Plot')
		p.grid(True,which='both')
		p.draw()
		p.pause(0.01)
	if(powerfunc==0):
		y = A*abs(np.sin(freq*(x*2.0*math.pi/1000.0)))+M
		p.plot(x,y)
		p.title('|Sine| Plot')
		p.xlabel('Time')
		p.ylabel('Amplitude')
		p.grid(True,which='both')
		p.draw()
		p.pause(0.01)
plotbutton = tk.Button(root,text="Plot",width=10,height=5,bg="blue",fg="white",command=plot)
plotbutton.grid(column=3,row=2)

s = tk.Scale(root,label="BPM",length=100,from_=0.0,to=60.0,digits=2,resolution=1)
s.grid(column=0,row=2)

sa = tk.Scale(root,label="Amplitude",length=100,from_=0,to=100,digits=3,resolution=1)
sa.grid(column=1,row=2)

sm = tk.Scale(root,label="Minimum",length=100,from_=0,to=100,digits=3,resolution=1)
sm.grid(column=2,row=2)

root.mainloop()
