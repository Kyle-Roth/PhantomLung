
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame,Label
from time import sleep

class MainWindow:

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
        
        #setting variable to the window
        settings=self.settings= Frame(root)
        settings.pack(expand='yes')

        # Make Slider Bars
        off=self.offset= Scale(settings,from_=0, to=100, orient='horizontal',label = 'Offset')
        amp=self.amp = Scale(settings,from_=0, to=100, orient='horizontal',label = 'Amp')
        bpm=self.bpm = Scale(settings,from_=0, to=50, orient='horizontal',label = 'BPM')
        off.grid(column=0,row=0)
        amp.grid(column=1,row=0)
        bpm.grid(column=2,row=0)

        variable= StringVar(settings)
        variable.set("|sin|") # default value for dropdown menu

        #makes the drop down menu and buttons
        mode = OptionMenu(settings, variable, "sin^2","sin^4","sin^6","|sin|",command=self.callback)
        start = self.start = Button(settings, text ="Start", command = self.start)
        update = self.update = Button(settings,text="Update",command=self.updatef)
        mode.grid(column=3,row=0)
        start.grid(column=4,row=0)
        update.grid(column=5,row=0)
        
        #makes all the text/labels in the GUI
        operationlabel = self.operationlabel = Label(settings,width=100,justify="left",fg="blue",text="Basic Operation Insturctions:")
        basicoperation = self.basicoperation = Label(settings,width=100,justify="left",text="Press start to begin robot motion.\nStart also works as a pause button. The currently selected values will be read in when start is pressed.\nUpdate will read in the currently selected values without pausing.\nThe robot will reset to the selected offset when updating or starting/unpausing before beginning the selected motion.")
        warninglabel = self.warninglabel = Label(settings,width=100,justify="left",fg="red",text="Operation Warning:")
        warning = self.warning = Label(settings,width=100,justify="left",text="Make sure the Amp and Offset sliders do not add to higher than 100 when reading into the calculations.\nThe program will give an error message and pause until valid values are passed in.")
        otherlabel = self.otherlabel = Label(settings,width=100,justify="left",fg="green",text="Other Useful Info:")
        other = self.other = Label(settings,width=100,justify="left",text="BPM stands for breaths per minute.\nAmp and Offset are input as a percentage of the maximum range of motion.\nThe maximum range of motion is approximately 3cm")
        operationlabel.grid(column=0,columnspan=6,row=1)
        basicoperation.grid(column=0,columnspan=6,row=2)
        warninglabel.grid(column=0,columnspan=6,row=3)
        warning.grid(column=0,columnspan=6,row=4)
        otherlabel.grid(column=0,columnspan=6,row=5)
        other.grid(column=0,columnspan=6,row=6)
        
    def callback(self,modeselect): #updates an intermediate function value whenever a dropdown menu option is selected
        self.FUNCinternal = modeselect
        print(modeselect)
        
    def updatef(self): #stores slider bar values and the intermediate function into the variables that the parent program accesses for calculations in servos 
        self.OFF = self.offset.get()*0.77+21
        self.AMP = self.amp.get()*0.77
        self.BPM = self.bpm.get()
        self.FUNC = self.FUNCinternal
        self.UpdateCheck = 1 #tells the parent program run the update branch
    
    def start(self): #function the start/stop button calls
        if self.running:
            self.running = 0 #tells parent program to pause
            self.start.configure(text='Start')
            print("Stoping")
        else:
            self.running = 1 #tells parent program to start/resume
            self.start.configure(text='Stop')
            print("Starting")
        self.updatef()
        
    def _close(self): #window close protocol
        self.running = 0
        self.UpdateCheck = 1
        self.root.destroy()
    
if __name__ == "__main__": #just for testing, not used when parent program runs
  
    root = tk.Tk()
    Window = MainWindow(root)
    root.update()
