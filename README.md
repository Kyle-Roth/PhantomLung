# Installation of Python 3 Requirements
First, ensure that you valid python3 installation.

To install the additional libraries neccesary for the program, run the following in commandline:
> pip3 install --user  -r "requirements.txt"

In case they should become useful, we have included many variations of the control software from throughout the design process. Following is a list of these versions and accompanying instructions.

# Raspberry Pi

Inside the 'NoGraph' folder are programs to run the Phantom Lung. These functions only have the controls and produce no graph. When using the PI, this is the recommended version. To run this, type
> python3 DNFM.py

Inside the 'RPi' folder are more programs to run the sensor and Lung on the Raspberry Pi. These functions produce a graph of the data. They are not recommended, but included for completness.
 DNFM.py should do no plotting
 DNFM2.py should plot both data sets

Inside the 'threading' folder are even more programs used to run the sensor and Lung. We were attempting to make the code threaded. This would ideally smooth the function of the Lung. This code never made it out of the Alpha phase... threading is stupid in python. And this code is acctually being altered to turn into muliprocessing instead of threading.

# Arduino

Inside the 'Arduino' folder is code to control the Lung using an Arduino. The Arduino is sent serial data from a laptop and the arduino makes this into a PWM signal. There are many different ways to run this code:
> python3 DNFMServo.py

> python3 DNFMEvo.py

This will open two seperate windows. The DNFMServo window can control the Lung and the DNFMEvo window can plot the data from the Sensor.
> python3 DNFM.py

This will run the Lung and Sensor and atttempt to plot both


# Sensor only

In the 'TeraRanger_Evo' folder, there is programs to control the Sensor only. In the 'TeraRanger_Evo' folder, there is a C program to take data from the sensor and write it to a Binary file. This was tested on a macbook. However, it should run in linux as well.
