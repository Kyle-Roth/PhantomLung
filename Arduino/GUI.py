
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk, Scale, Button, OptionMenu, StringVar, Frame
from time import sleep
from TeraRanger_Evo_UART import TeraRanger

class MainWindow:


    eline = None
    sline = None
    ExitFlag = 1
    running = 0
    update = 0
    OFF = 0
    AMP = 0
    BPM = 0
    FUNC = "|sin|"

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

        self.listVar = variable= StringVar(settings)
        variable.set("|sin|") # default value

        mode = OptionMenu(settings, variable, "sin^2","sin^4","sin^6","|sin|",command=self.callback)
        start = self.start = Button(settings, text ="Start", command = self.start)
        update = self.update = Button(settings,text="Update",command=self.updatef)
        mode.grid(column=3,row=0)
        start.grid(column=4,row=0)
        update.grid(column=5,row=0)

    def callback(self,modeselect):
        self.FUNC = modeselect
        print(modeselect)

    def updatef(self):
        self.OFF = self.offset.get()
        self.AMP = self.amp.get()
        self.BPM = self.bpm.get()
        self.FUNC = self.listVar.get()
        self.update = 1

    def updatePlots(self,sTime,sData,eTime,eData):
        ax = self.ax
        canvas = self.canvas

        if self.sline == None or self.eline == None:
            ax.clear()
            self.sline, = ax.plot(sTime,sData,'b')
            self.eline, = ax.plot(eTime,eData,'r')
            # self.txt, = ax.text(0.83, 1.02,f'{bpm:.2f} bpm',
            #         color = 'b', fontsize = 20,
            #         bbox={'facecolor': 'blue', 'alpha': 1, 'pad': 3},
            #         transform = ax.transAxes)

            ax.set_ylim([0, 100])
            ax.set_xlim([min(sTime[0],eTime[0]), max(sTime[-1],eTime[-1])])


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

            ax.set_xlim([min(sTime[0],eTime[0]), max(sTime[-1],eTime[-1])])


            # restore the background, draw animation,blit
            canvas.restore_region(self.background)
            ax.draw_artist(ax.get_xaxis())
            ax.draw_artist(self.sline)
            ax.draw_artist(self.eline)
            canvas.blit(ax.clipbox)
            canvas.flush_events()

    def updatePlot(self,sTime,sData):
        ax = self.ax
        canvas = self.canvas

        if self.sline == None:
            ax.clear()
            self.sline, = ax.plot(sTime,sData,'b')
            # ax.text(0.83, 1.02,f'{bpm:.2f} bpm',
            #         color = 'b', fontsize = 20,
            #         bbox={'facecolor': 'blue', 'alpha': 1, 'pad': 3},
            #         transform = ax.transAxes)

            ax.set_ylim([0, 100])
            ax.set_xlim([sTime[0], sTime[-1]])


            # set animation, save backgorund
            ax.get_xaxis().set_animated(True)
            self.sline.set_animated(True)
            canvas.draw()
            self.background=canvas.copy_from_bbox(ax.get_figure().bbox)

            # now redraw and blit
            ax.draw_artist(ax.get_xaxis())
            ax.draw_artist(self.sline)
            canvas.blit(ax.clipbox)

        else:
            self.sline.set_xdata(sTime)
            self.sline.set_ydata(sData)

            ax.set_xlim([sTime[0], sTime[-1]])


            # restore the background, draw animation,blit
            canvas.restore_region(self.background)
            ax.draw_artist(ax.get_xaxis())
            ax.draw_artist(self.sline)
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
        self.ExitFlag = 0
        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()
    Window = MainWindow(root)

    while(Window.ExitFlag):
        root.update()
