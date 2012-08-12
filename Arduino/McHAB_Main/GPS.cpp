#include "GPS.h"

//Variable declaration

SoftwareSerial mySerial(8,9);
String gpsData;

//functions' bodies
void initializeGPS(){
	mySerial.begin(4800);
}
void readGPS()
{
  char readValue = '\0';
  gpsData = "";
  
  while(mySerial.available())
  {
    readValue = mySerial.read();
    gpsData += readValue;
  }
 
  Serial.print(gpsData);
}


