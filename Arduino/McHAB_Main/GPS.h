#ifndef GPS_h
#define GPS_h

#include <SoftwareSerial.h>
#include <Wire.h>
#include <Arduino.h>

//function declaration

void readGPS();
void initializeGPS();
void getGPGGA();

//variable declaration

extern SoftwareSerial mySerial;
extern bool dataReady;
extern String gpsData;
extern String gpgga;
#endif
