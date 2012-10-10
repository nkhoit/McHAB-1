#ifndef GPS_h
#define GPS_h

#include <SoftwareSerial.h>
#include <Wire.h>
#include <Arduino.h>

//function declaration

void readGPS(String &GPSgpgga);
void initializeGPS();
void getGPGGA(String &GPSgpgga);

//variable declaration

extern SoftwareSerial mySerial;
extern bool gpsDataReady;
extern String gpsData;
extern String gpgga;
#endif
