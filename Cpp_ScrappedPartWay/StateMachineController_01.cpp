#include <iostream>
#include <stdlib.h>
#include <stdio.h>
using namespace std;

int main() {
   //int age;
   //cin >> age;
   //cout << age;
   int state;
   state = 1;
   while (1){
    switch(state) {
        case 1:
            cout << "State selection initiated." << endl;
            cout << "Please select the state you wish to run: ";
            cin >> state;
            break;
        case 2:
            cout << "state 2 now running";
            break;
        case 0:
        return 0;
        default:
            cout << "Invalid State." << endl;
            cout << "Please input a different state, or enter 0 to end the program." << endl;
            cin >> state;
            break;
        }
    }
   return 0;
}
