







import serial
import math
import numpy as np
import serial.tools.list_ports
import crcmod.predefined  # To install: pip install crcmod
from time import sleep,time
import tkinter as tk
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame
import RPi.GPIO as GPIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar

import threading
from scipy.fftpack import fft, fftfreq

sData = []
eData = []
sTime = []
eTime = []

class MainWindow:

	t = np.linspace(0, 2, 2 * 10000, endpoint=False)
	f = 1
	line = None
	running = 0
	OFF = 0
	AMP = 0
	BPM = 0
	FUNCinternal = "|sin|"
	FUNC = "|sin|"
	UpdateCheck = 0

	def __init__(self,root):

		self.root = root

		# Set gentle close
		root.protocol("WM_DELETE_WINDOW", self._close)  # easy kill program

		# Create Figure and Pack Axis
		fig=self.fig = Figure(figsize=(8,6))
		ax=self.ax = fig.add_subplot(111)
		canvas=self.canvas = FigureCanvasTkAgg(fig, root) # A tk.DrawingArea
		self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1) # Add fig to Tk Window

		ax.grid(which='both',linestyle='--')
		ax.set_xlabel("Time (s)")

		settings=self.settings= Frame(root)
		settings.pack(expand='yes')

		# Make Slider Bars
		off=self.offset= Scale(settings,from_=0, to=100,
							   orient='horizontal',label = 'Offset')
		amp=self.amp = Scale(settings,from_=0, to=100,
							 orient='horizontal',label = 'Amp')
		bpm=self.bpm = Scale(settings,from_=0, to=50,
							 orient='horizontal',label = 'BPM')
		off.grid(column=0,row=0)
		amp.grid(column=1,row=0)
		bpm.grid(column=2,row=0)

		variable= StringVar(settings)
		variable.set("|sin|") # default value

		mode = OptionMenu(settings, variable, "sin^2","sin^4","sin^6","|sin|",command=self.callback)
		start = self.start = Button(settings, text ="Start", command = self.start)
		update = self.update = Button(settings,text="Update",command=self.updatef)
		mode.grid(column=3,row=0)
		start.grid(column=4,row=0)
		update.grid(column=5,row=0)

	def callback(self,modeselect):
		self.FUNCinternal = modeselect
		print(modeselect)
	def updatef(self):
		self.OFF = self.offset.get()*0.77+21
		self.AMP = self.amp.get()*0.77
		self.BPM = self.bpm.get()
		self.FUNC = self.FUNCinternal
		self.UpdateCheck = 1

	def updatePlot(self,sTime,sData,eTime,eData):
		t = self.t
		f = self.f
		ax = self.ax
		canvas = self.canvas

		if self.line == None:
			self.sline, = ax.plot(sTime,sData,'b')
			self.eline, = ax.plot(eTime,eData,'r')

			ax.text(0.83, 1.02,'25 bpm',
					color = 'b', fontsize = 20,
					# bbox={'facecolor': 'blue', 'alpha': 1, 'pad': 3},
					transform = ax.transAxes)

			#ax.relim()
			#ax.autoscale_view()

			#canvas.draw()
			#canvas.draw()
			#canvas.flush_events()
			ax.set_ylim([0, 100])
			ax.set_xlim([min(sTime[0],eTime[0]), max(sTime[len(sTime)-1],eTime[len(eTime)-1])])


			# set animation, save backgorund
			ax.get_xaxis().set_animated(True)
			self.sline.set_animated(True)
			self.eline.set_animated(True)
			canvas.draw()
			self.background=canvas.copy_from_bbox(ax.get_figure().bbox)

			# now redraw and blit
			ax.draw_artist(ax.get_xaxis())
			ax.draw_artist(self.sline)
			ax.draw_artist(self.eline)
			canvas.blit(ax.clipbox)

		else:
			self.sline.set_xdata(sTime)
			self.sline.set_ydata(sData)
			self.eline.set_xdata(eTime)
			self.eline.set_ydata(eData)

			ax.set_xlim([min(sTime[0],eTime[0]), max(sTime[len(sTime)-1],eTime[len(eTime)-1])])


			# restore the background, draw animation,blit
			canvas.restore_region(self.background)
			ax.draw_artist(ax.get_xaxis())
			ax.draw_artist(self.sline)
			ax.draw_artist(self.eline)
			canvas.blit(ax.clipbox)
			canvas.flush_events()

	def start(self):
		if self.running:
			self.running = 0
			self.start.configure(text='Start')
			print("Stoping")
		else:
			self.running = 1
			self.start.configure(text='Stop')
			print("Starting")
		self.updatef()

	def _close(self):
		self.running = 0
		self.UpdateCheck = 1
		self.root.destroy()


class servofunctions:
	start = 0.0
	freq = 0
	A = 0
	M = 21
	t = 21
	data = []
	time = []
	#range 21 to 98 (roughly 30mm)
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

class TeraRanger(threading.Thread):
	port = None
	evo = None
	data = []
	time = []
	start = 0
	freqs = []
	bpm = None
	min = 100
	max = 0

	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "Sensor Thread"
		print('Initializing Evo Data Stream')

		self.port = self.findEvo()

		if self.port == 'NULL':
			print("Could not find Evo")
		else:
			print("Found Evo")
			self.evo = self.openEvo()

	def run(self):
		self.reset()
		self.streamData()


	def findEvo(self):
		# Find Live Ports, return port name if found, NULL if not
		print('Scanning all live ports on this PC')
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			# print p # This causes each port's information to be printed out.
			if "5740" in p[2]:
				print('Evo found on port ' + p[0])
				return p[0]
		return 'NULL'

	def reset(self):
		self.min = 100
		self.max = 0
		self.start = time()
		self.data = []
		self.time = []

	def openEvo(self):
		portname = self.port
		print('Attempting to open port...')
		# Open the Evo and catch any exceptions thrown by the OS
		print(portname)
		self.evo = serial.Serial(portname, baudrate=115200, timeout=2)
		# Send the command "Binary mode"
		set_bin = (0x00, 0x11, 0x02, 0x4C)
		# Flush in the buffer
		self.evo.flushInput()
		# Write the binary command to the Evo
		self.evo.write(set_bin)
		# Flush out the buffer
		self.evo.flushOutput()
		print('Serial port opened')
		return self.evo

	def get_evo_range(self):
		evo_serial = self.evo
		crc8_fn = crcmod.predefined.mkPredefinedCrcFun('crc-8')
		# Read one byte
		evo_serial.flushInput()
		data = evo_serial.read(1)
		if data == b'T':
			# After T read 3 bytes
			frame = data + evo_serial.read(3)
			if frame[3] == crc8_fn(frame[0:3]):
				# Convert binary frame to decimal in shifting by 8 the frame
				rng = frame[1] << 8
				rng = rng | (frame[2] & 0xFF)
			else:
				print("CRC mismatch. Check connection or make sure only one progam access the sensor port.")
				rng = 0
		# Check special cases (limit values)
		else:
			print("Waiting for frame header")
			rng = 0

		# Checking error codes
		#if rng == 65535: # Sensor measuring above its maximum limit
		#	dec_out = float('inf')
		#elif rng == 1: # Sensor not able to measure
		#	dec_out = float('nan')
		#elif rng == 0: # Sensor detecting object below minimum range
		#	dec_out = -float('inf')
		#else:
			# Convert frame in meters
		#	dec_out = rng / 1000.0


		if rng == 65535 or rng == 1 or rng == 0:
			dec_out = 0
		else:
			dec_out = rng / 1000.0

		return dec_out



	def update(self):
		# append to data array
		self.data.append(self.get_evo_range())
		self.data = self.data[-100:]

		# append to time array
		self.time.append(time()-self.start)
		self.time = self.time[-100:]

	def getData(self):
		global edata
		mi = min(self.data)
		ma = max(self.data)


		if mi < self.min and mi != 0:
			self.min = mi
		if ma > self.max:
			self.max = ma


		temp = [0 for i in range(len(self.data))]

		if self.max > 0:
			if self.max != self.min:
				for i in range(len(temp)):
					#temp[i] = (temp[i]-mi)*(100/ma)
					temp[i] = 100-(self.edata[i]-self.min)/(self.max-self.min)*100
			else:
				temp = self.edata

		return temp

	def streamData(self):
		global eData
		global eTime

		print('Starting Evo Data Stream')

		while True:
			try:
				# append to data array
				eData.append(self.get_evo_range())
				eData = eData[-100:]

				# append to time array
				eTime.append(time()-self.start)
				eTime = eTime[-100:]

			except serial.serialutil.SerialException:
				print("Device disconnected (or multiple access on port). Exiting...")
				break

	def _close(self):
		self.evo.close()

def switch(arg):
	switcher = { "|sin|":servo.absolute,"sin^2":servo.squared,
		"sin^4":servo.fourth,"sin^6":servo.sixth}
	return switcher.get(arg,"invalid")

if __name__=='__main__':
	#servo = servofunctions()
	evot = TeraRanger()
	#func = servo.absolute
	#root = tk.Tk()
	#Window = MainWindow(root)

	evot.start()
	
	while(1):
		print(eData)

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
