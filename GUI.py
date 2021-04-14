

import tkinter as tk



class MainWindow:

    def __init__(self,root):

        self.root = root

        fig=self.fig = Figure(figsize=(8,6))
        ax=self.ax = fig.add_subplot(111)
        canvas=self.canvas = FigureCanvasTkAgg(fig, root) # A tk.DrawingArea
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1) # Add fig to Tk Window
        root.protocol("WM_DELETE_WINDOW", self._close)  # easy kill program


    def updatePlot():
        t = linespace()
        self.lines = ax.plot()

    def _close(self):
        self.root.destroy()
