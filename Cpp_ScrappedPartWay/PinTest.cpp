#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>
#define _USE_MATH_DEFINES
#include <math.h>

using namespace std;

int main (void) 
	{
	int t;
	int tt;
	int i = 0;
	wiringPiSetup();
	pinMode (1, PWM_OUTPUT);
	pinMode (23, PWM_OUTPUT);
	//pinMode (27, OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(50);
	while(1)
	{	
			i++;
			t = (int)abs(802*sin(0.69*((double) i/217.299549)))+172;
			tt = 802*pow(sin(1*((double) i*2*M_PI/1000.0)),2)+172;
			//tt = abs(802*sin(0.42*((double) i*2*M_PI/1000.0)))+172; //0.42 max freq
			pwmWrite(1,t);
			//cin >> tt;
			pwmWrite(23,tt);
			delayMicroseconds(1000);
			if(i%20 == 0)
			{ 
				cout << M_PI << " " << tt << " " << i << endl;			
			}	
}
	return 0;
}
