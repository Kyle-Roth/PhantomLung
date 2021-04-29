
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame
from time import sleep
from TeraRanger_Evo_UART import TeraRanger

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

    def updatePlot(self,time,data):
        t = self.t
        f = self.f
        ax = self.ax
        canvas = self.canvas

        if self.line == None:
            self.line, = ax.plot(time,data,'b')
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
            ax.set_xlim([time[0], time[len(time)-1]])


            # set animation, save backgorund

            ax.get_xaxis().set_animated(True)
            self.line.set_animated(True)
            canvas.draw()
            self.background=canvas.copy_from_bbox(ax.get_figure().bbox)

            # now redraw and blit
            ax.draw_artist(ax.get_xaxis())
            ax.draw_artist(self.line)
            canvas.blit(ax.clipbox)

        else:
            self.line.set_xdata(time)
            self.line.set_ydata(data)
            self.ax.set_xlim([time[0],time[len(time)-1]])


            #canvas.draw()
            #canvas.flush_events()

            # restore the background, draw animation,blit
            canvas.restore_region(self.background)
            ax.draw_artist(ax.get_xaxis())
            ax.draw_artist(self.line)
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

if __name__ == "__main__":

    root = tk.Tk()
    Window = MainWindow(root)
    Evo = 5 #TeraRanger()
    while(1):
        root.update()
    updatePlots(Window,Window)
