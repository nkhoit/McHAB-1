#ifndef GPS_h
#define GPS_h

#include <SoftwareSerial.h>
#include <Wire.h>
#include <Arduino.h>

//function declaration

void readGPS();
void initializeGPS();

//variable declaration

extern SoftwareSerial mySerial;
extern String gpsData;

#endif