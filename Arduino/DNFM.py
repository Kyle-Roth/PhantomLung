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
	evo = TeraRanger()
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
			evo.reset()
			Window.update = 0

		elif Window.running:
			servo.update()
			evo.update()
			Window.updatePlots(servo.time,servo.data,evo.time,evo.getData())

		root.update()

	servo._close()
	evo._close()
