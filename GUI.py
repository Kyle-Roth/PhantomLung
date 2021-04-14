
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
from tkinter import Tk

class MainWindow:

    t = np.linspace(0, 2, 2 * 10000, endpoint=False)
    f = 1
    lines = None

    def __init__(self,root):

        self.root = root

        fig=self.fig = Figure(figsize=(8,6))
        ax=self.ax = fig.add_subplot(111)
        canvas=self.canvas = FigureCanvasTkAgg(fig, root) # A tk.DrawingArea
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1) # Add fig to Tk Window
        root.protocol("WM_DELETE_WINDOW", self._close)  # easy kill program

        ax.grid(which='both',linestyle='--')

        self.updatePlot()


    def updatePlot(self):
        t = self.t
        f = self.f
        ax = self.ax
        lines = self.lines
        if lines == None:
            y = np.sin(f * 2 * np.pi * t)
            x = np.sin(10/f * 2 * np.pi * t)
            lines = ax.plot(t,x,'r',t,y,'b')
            ax.text(0.83, 1.02,'25 bpm',
                    color = 'b', fontsize = 20,
                    # bbox={'facecolor': 'blue', 'alpha': 1, 'pad': 3},
                    transform = ax.transAxes)
        else:
            f+=1;
            y = np.sin(f * 2 * np.pi * t)
            x = np.sin(10/f * 2 * np.pi * t)

            lines[0].set_ydata(x)
            lines[1].set_ydata(y)

    def _close(self):
        self.root.destroy()



if __name__ == "__main__":

    root = tk.Tk()
    Window = MainWindow(root)
    root.mainloop()
