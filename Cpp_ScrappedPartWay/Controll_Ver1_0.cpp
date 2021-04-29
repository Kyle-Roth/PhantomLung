#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <fstream>
#include <cstdlib>
#define _USE_MATH_DEFINES
#include <cmath>
#include <wiringPi.h>

using namespace std;

int main(void){
//set up for wiringPi
	wiringPiSetup();
	pinMode (23, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(50);
	pwmWrite(23,172);
	int t;
	int i = 0; //general iteration function
	int state = 1; //initializing state to go to select mode
	int f = 0; //state variable for slecting between defualt waveform and file input waveform
	int k = 0; //iteration for exponential function
	double freq; //frequency
	while(1){
		switch(state) { //first layer of switch case - add new waveforms on this layer - basic format can be seen in case 2
			case 1: //initial case - chooses function
				cout << "Mode selection initiated.\n";
				cout << "Modes: 0 - Ends program, 1 - Stays in mode selection, 2 - abs|sin(f*x)|, 3 - sin^2(f*x), 4 - sin^6(f*x), 5 - Exponential Mode, 6[More to be added]\n";
				cin >> state;
				break; //break statement runs loop again to update which case is being ran
			case 2: //absolute value of sine - also can be used as a format for new waveforms
				cout << "Absolute value of sine mode chosen.\n"; //tells the user which mode they chose
				cout << "Enter 0 to use the default waveform. Enter 1 to use custom variables for the waveform.\n"; //gives instructions for waveform selection
				cin >> f; //input for which waveform format
				cout << "Use ctrl+c to end program.\n"; //info on how to quit out
				switch(f){ //second layer of switch case - selects between default and custom waveform
					case 0: //default waveform
						while(1){ //this loop controls the servo(s)
							i++;
							t = abs(800*sin(0.2*((double)i*2.0*M_PI/1000.0)))+172; //0.42 max freq; frequency is half of breathing frequency
							//cout << t << endl;
							//cmath works. math.h doesn't for some reason
							pwmWrite(23,t); //writes to the pin being used - pinout can be looked up online
							delayMicroseconds(1000); //delay of loop in microseconds - included in frequency calculation
						}
					case 1: //custom waveform - adjustable frequency - adjustable amplitude to be added				
						freq = 0;						
						cout << "Enter a frequncy from 0 to 0.42. Note that the frequncy here is half of the breathing frequency.\n"; //frequency limit based off experimentation - limit is likely due to limit in step size and servo movement speed between steps of certain lengths apart
						cin >> freq; //frequency input
						while(1){ //loop controls servo
							i++;
							t = abs(800*sin(freq*(((double)i*2.0*M_PI/1000.0))))+172; //0.42 max freq
							pwmWrite(23,t);
							delayMicroseconds(1000);
						}
					default: //returns to first layer mode selection intialization when neither default or custom waveform are picked
						cout << "That was not a 1 or 0. Returning to main mode selection.\n";
						state = 1;
						break;
					}
				break;
			case 3:
				cout << "Sine squared mode chosen.\n";
				cout << "Enter 0 to use the default waveform. Enter 1 to use custom variables for the waveform.\n";
				cin >> f;
				cout << "Use ctrl+c to end program.\n";
				switch(f){
					case 0: //default waveform
						while(1){
							i++;
							t = 800*pow(sin(0.125*((double)i*2.0*M_PI/1000.0)),2)+172; //1 max freq
							//cout << t << endl;
							pwmWrite(23,t);
							delayMicroseconds(1000);
						}
					case 1: //custom waveform - adjustable frequency - adjustable amplitude to be added				
						freq = 0;						
						cout << "Enter a frequncy from 0 to 1. Note that the frequncy here is half of the breathing frequency.\n";
						cin >> freq;
						while(1){
							i++;
							t = 800*pow(sin(freq*((double)i*2.0*M_PI/1000.0)),2)+172; //1 max freq
							pwmWrite(23,t);
							delayMicroseconds(1000);
						}
					default:
						cout << "That was not a 1 or 0. Returning to main mode selection.\n";
						state = 1;
						break;
					}
				break;
			case 4:
				cout << "Sine^6 mode chosen.\n";
				cout << "Enter 0 to use the default waveform. Enter 1 to use custom variables for the waveform.\n";
				cin >> f;
				cout << "Use ctrl+c to end program.\n";
				switch(f){
					case 0: //default waveform
						while(1){
							i++;
							t = 800*pow(sin(0.125*((double)i*2.0*M_PI/1000.0)),6)+172; //1 max freq
							pwmWrite(23,t);
							//cout << t << "   " << i << endl;
							delayMicroseconds(1000);
						}
					case 1: //custom waveform - adjustable frequency - adjustable amplitude to be added				
						freq = 0;						
						cout << "Enter a frequncy from 0 to 1. Note that the frequncy here is half of the breathing frequency.\n";
						cin >> freq;
						while(1){
							i++;
							t = 800*pow(sin(freq*((double)i*2.0*M_PI/1000.0)),6)+172; //1 max freq
							pwmWrite(23,t);
							delayMicroseconds(1000);
						}
					default:
						cout << "That was not a 1 or 0. Returning to main mode selection.\n";
						state = 1;
						break;
					}
				break;
			case 5:
				cout << "Exponential mode chosen.\n";
				cout << "Enter 0 to use the default waveform. Enter 1 to use custom variables for the waveform.\n";
				cin >> f;
				cout << "Use ctrl+c to end program.\n";
				switch(f){
					case 0: //default waveform
						while(1){
							i++;
							k++;
							if (k > 1500) k = 0; 
							if (k < 501) {
								t = 800*(1.0-exp(-k/50.0))+172;
							}
							if (k > 500) {
								t = 800*exp(-(k-500.0)/250.0)+172;
							}
							//cout << t << "   " << k << endl;
							pwmWrite(23,t);
							delayMicroseconds(1000);
						}
					/*case 1: //custom waveform - adjustable frequency - adjustable amplitude to be added				
						freq = 0;						
						cout << "Enter a frequncy from 0 to 1. Note that the frequncy here is half of the breathing frequency.\n";
						cin >> freq;
						while(1){
							i++;
							t = 802*pow(sin(freq*((double)i*2*M_PI/1000.0)),2)+172; //1 max freq
							pwmWrite(23,t);
							delayMicroseconds(1000);
						}*/
					default:
						cout << "That was not a 1 or 0. Returning to main mode selection.\n";
						state = 1;
						break;
					}
				break;

			case 0:
				return 0;
			default: //loops back to mode selection if invalid mode is selected
				cout << "Invalid state.\n";
				cout << "Please input a different state, or enter 0 to end the program.\n";
				cin >> state;
				break;
			}
		}
	return 0;
}			

