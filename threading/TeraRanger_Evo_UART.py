#!/usr/bin/env python3
###### TeraRanger Evo Example Code STD #######
#                                            #
# All rights reserved Terabee France (c) 2018#
#                                            #
############ www.terabee.com #################

import serial
import numpy as np
import serial.tools.list_ports
import crcmod.predefined  # To install: pip install crcmod
from time import time
from threading import Thread


from scipy.fftpack import fft, fftfreq


class TeraRanger(Thread):

    port = None
    evo = None
    data = []
    time = []
    startTime = 0
    freqs = []
    bpm = None
    min = 100
    max = 0
    
    updateCheck = 0
    running = 1
    
    def __init__(self):
        
        Thread.__init__(self)
        print('Initializing Evo Data Stream')

        self.port = self.findEvo()
        
        if self.port == 'NULL':
            print("Could not find Evo")
        else:
            print("Found Evo")
            self.evo = self.openEvo()
            
    def run(self):
        self.reset()
        
        while True:
            if self.updateCheck:
                self.reset()
                self.updateCheck = 0
            elif self.running:
                try:
                    self.plotCheck = 0
                    
                    # append to data array
                    self.data.append(self.get_evo_range())
                    self.data = self.data[-100:]
                    
                    # append to time array
                    self.time.append(time()-self.startTime)
                    self.time = self.time[-100:]
                    
                    self.plotCheck = 1
                except serial.serialutil.SerialException:
                   print("Device disconnected (or multiple access on port). Exiting...")
                   break

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
        self.startTime = time()
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
        #    dec_out = float('inf')
        #elif rng == 1: # Sensor not able to measure
        #    dec_out = float('nan')
        #elif rng == 0: # Sensor detecting object below minimum range
        #    dec_out = -float('inf')
        #else:
            # Convert frame in meters
        #    dec_out = rng / 1000.0
        
        
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
        self.time.append(time()-self.startTime)
        self.time = self.time[-100:]
    
    def getData(self):
        mi = min(self.data)
        ma = max(self.data)
        
        
        if mi < self.min and mi != 0:
            self.min = mi
        if ma > self.max:
            self.max = ma
            
            
        temp = [0 for i in range(len(self.data))]
        
        if self.max > 0:
            if self.max != self.min:
                for i in range(len(data)):
                    #temp[i] = (temp[i]-mi)*(100/ma)
                    temp[i] = 100-(self.data[i]-self.min)/(self.max-self.min)*100
            else:
                temp = self.data    

        return temp

    def _close(self):
        self.evo.close()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from time import sleep, process_time
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk # custom toolbar
    from tkinter import Tk

    evo = TeraRanger()
    evo.startTime = time()
    
    root = Tk()
        # Create Figure and Pack Axis
    fig = Figure(figsize=(8,6))
    ax= fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, root) # A tk.DrawingArea
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1) # Add fig to Tk Window
    
    ax.grid(which='both',linestyle='--')
    ax.set_xlabel("Time (s)")
    
    line, = ax.plot(evo.time,evo.data)
    ax.set_ylim([0,100])
    
    ax.get_xaxis().set_animated(True)
    #ax.get_yaxis().set_animated(True)
    line.set_animated(True)
    canvas.draw()
    background=canvas.copy_from_bbox(fig.bbox)

    # now redraw and blit
    ax.draw_artist(ax.get_xaxis())
    ax.draw_artist(line)
    canvas.blit(ax.clipbox)

    
    while True:
        evo.update()
        
        line.set_xdata(evo.time)
        line.set_ydata(evo.getData())
        ax.set_xlim([evo.time[0],evo.time[len(evo.time)-1]])
        #ax.set_ylim([max(evo.data),min(evo.data)])
                            
        # restore the background, draw animation,blit
        canvas.restore_region(background)
        ax.draw_artist(ax.get_xaxis())
        #ax.draw_artist(ax.get_yaxis())
        ax.draw_artist(line)
        canvas.blit(ax.clipbox)
        canvas.flush_events()
