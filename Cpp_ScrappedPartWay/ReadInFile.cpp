#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <fstream>
#include <cstdlib>
#include <math.h>
#include <wiringPi.h>
using namespace std;

int main(void) {
	wiringPiSetup();
	ifstream indata;
	double e;
	char t[20];
	cout << t << endl;
	cout << "Insert desired data file name: ";
	cin >> t;
	cout << endl;
	indata.open(t);
	if(!indata)	{
		cerr << "Error: File could not be opened.\n";
		exit(1);
	}
	indata >> e;
	while(!indata.eof()) {	
		cout << e << endl;
		indata >> e;
		delayMicroseconds(100000);
	}
	indata.close();
	cout << "All numbers printed.\n";
	return 0;
}
