
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

        settings=self.settings= Frame(root)
        settings.pack(expand='yes')

        # Make Slider Bars
        off=self.offset= Scale(settings,from_=0, to=200,
                               orient='horizontal',label = 'Offset')
        amp=self.amp = Scale(settings,from_=0, to=200,
                             orient='horizontal',label = 'Amp')
        bpm=self.bpm = Scale(settings,from_=0, to=200,
                             orient='horizontal',label = 'bpm')
        off.grid(column=0,row=0)
        amp.grid(column=1,row=0)
        bpm.grid(column=2,row=0)

        variable = StringVar(settings)
        variable.set("one") # default value

        mode = OptionMenu(settings, variable, "one", "two", "three")
        start = self.start = Button(settings, text ="Start", command = self.start)
        mode.grid(column=3,row=0)
        start.grid(column=4,row=0)

        self.updatePlot()


    def updatePlot(self):
        t = self.t
        f = self.f
        ax = self.ax
        line = self.line
        if line == None:
            y = np.sin(f * 2 * np.pi * t)
            # x = np.sin(10/f * 2 * np.pi * t)
            self.line, = ax.plot(t,y,'b')
            ax.text(0.83, 1.02,'25 bpm',
                    color = 'b', fontsize = 20,
                    # bbox={'facecolor': 'blue', 'alpha': 1, 'pad': 3},
                    transform = ax.transAxes)
        else:
            f+=1;
            y = np.sin(f * 2 * np.pi * t)
            x = np.sin(10/f * 2 * np.pi * t)

            line.set_ydata(x)
            # lines[1].set_ydata(y)

    def start(self):
        if self.running:
            self.running = 0
            self.start.configure(text='Start')
            print("Stoping")
        else:
            self.running = 1
            self.start.configure(text='Stop')
            print("Starting")

        # set animation, save backgorund
        self.line.set_animated(True)
        self.canvas.draw()
        self.background=self.canvas.copy_from_bbox(self.ax.bbox)

        # now redraw and blit
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)


        # while self.running:
        #     self.updatePlot()
        #
        #     # restore the background, draw animation,blit
        #     self.canvas.restore_region(self.background)
        #     self.ax.draw_artist(self.line)
        #     self.canvas.blit(self.ax.bbox)
        #     sleep(1)

    def _close(self):
        self.root.destroy()

def updatePlots(window,evo):

    # set animation, save backgorund
    window.line.set_animated(True)
    window.canvas.draw()`
    window.background=window.canvas.copy_from_bbox(window.ax.bbox)

    # now redraw and blit
    window.ax.draw_artist(window.line)
    window.canvas.blit(window.ax.bbox)


    while True:
        window.updatePlot()

        # restore the background, draw animation,blit
        window.canvas.restore_region(window.background)
        window.ax.draw_artist(window.line)
        window.canvas.blit(window.ax.bbox)

        root.after(2000,updatePlots, window, evo)



if __name__ == "__main__":

    root = tk.Tk()
    Window = MainWindow(root)
    Evo = 5 #TeraRanger()

    root.mainloop()
