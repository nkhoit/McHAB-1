//Arduino 1.0+ Only
//Arduino 1.0+ Only

/*Based largely on code by  Jim Lindblom

 Get pressure, altitude, and temperature from the BMP085.
 Serial.print it out at 9600 baud to serial monitor.
 */
#include <Wire.h>
#include <SPI.h>
#include "BMP.h"
#include "GPS.h"
#include "MPU6000.h"
#include "HMC5883.h"
#include <SoftwareSerial.h>

int SENSOR_SIGN[] = {1,-1,-1,-1,1,1,-1,1,-1};

//Miscellanous variables
int currentTime = 0; //Timer in milliseconds
int timer1 = 0; //Timer for 200hz
int timer2 = 0; //Timer for 5hz

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  SPI.begin();

  bmp085Calibration();
  initializeGPS();
  MPU6000_Init(); 
  HMC5883_init();
}  

void loop()
{
  currentTime = millis();
  
  // 200Hz 
  if(currentTime - timer1 >= 5)
  {
    Serial.println("BMP:  ");
    readBMP();
    Serial.println("-----------------------------------");
    Serial.println("MPU:  "); 
    MPU6000_Read();
    Serial.println("-----------------------------------");
    Serial.println("HMC5883:  ");
    HMC5883_read(); 
    timer1 = currentTime;
  }
  
  // 5Hz
  if(currentTime - timer2 >= 333)
  {
    Serial.println("GPS:  ");
    readGPS();
    timer2 = currentTime;
    Serial.println(); 
  }
  
  //Serial.println();  
}

void writeRegister(int deviceAddress, byte address, byte val) {
  Wire.beginTransmission(deviceAddress); // start transmission to device 
  Wire.write(address);       // send register address
  Wire.write(val);         // send value to write
  Wire.endTransmission();     // end transmission
}

int readRegister(int deviceAddress, byte address){

  int v;
  Wire.beginTransmission(deviceAddress);
  Wire.write(address); // register to read
  Wire.endTransmission();

  Wire.requestFrom(deviceAddress, 1); // read a byte

  while(!Wire.available()) {
    // waiting
  }

  v = Wire.read();
  return v;
}
/*
void readGPS()
{
  Serial.println("In readGPS");
  char readValue = '\0';
  gpsData = "";
  
  while(mySerial.available())
  {
    readValue = mySerial.read();
    gpsData += readValue;
  }
 
  Serial.print(gpsData);
}
*/

