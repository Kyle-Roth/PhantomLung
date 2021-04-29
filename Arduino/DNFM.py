import tkinter as tk

# Custom Libraries
from GUI import MainWindow
from servos import Servo
from TeraRanger_Evo_UART import TeraRanger

def updateParams(servo,window):
	servo.amp = window.AMP
	servo.min = window.OFF
	servo.bpm = window.BPM
	servo.func = servo.switch(window.FUNC)

if __name__=='__main__':
	servo = Servo("/dev/cu.usbserial-14130")
	# This is the Sensor. To adapt the code for a new sensor, Replace 'TeraRanger()' with
	# The constructor for your new sensor. This new sensor library will need to have funciton
	# calls for update(), reset(), close(), getData(), and there should be a time array
	sensor = TeraRanger()
	root = tk.Tk()
	Window = MainWindow(root)


	# Main Loop
	while(Window.ExitFlag):
		if Window.update:
			if Window.running:
				updateParams(servo,Window)
			else:
				servo.min = 0 #21 duty cycle corresponds with 0 location

			# Reset the needed parameters
			servo.reset()
			sensor.reset()
			Window.update = 0

		elif Window.running:
			servo.update()
			sensor.update()
			Window.updatePlots(servo.time,servo.data,sensor.time,sensor.getData())

		root.update()

	servo._close()
	sensor._close()
