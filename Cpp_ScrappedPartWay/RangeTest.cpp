#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>
#include <math.h>

using namespace std;

int main (void) 
	{
	int t = 160;
	int i = 0;
	int f = 0;
	wiringPiSetup();
	pinMode (1, PWM_OUTPUT);
	pinMode (23, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(50); //getting range of motion 33mm
	cin >> f;
	pwmWrite(23,f); //range of pwmWrite is from 172 to 972
	pwmWrite(1,f); //range of pwmWrite is from 172 to 972
	delayMicroseconds(100000);
		/*while(1)
		{	
			i++;
			if(t > 180) {
				t = 160;
			}
			t++;
			delayMicroseconds(1000000);
			pwmWrite(23,t);	
			cout << t << " " << (double)((double)t/1024.0)*100.0 << endl;				
	}	
	*/return 0;
}
