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
#include <SoftwareSerial.h>

//const unsigned char OSS = 0;  // Oversampling Setting

//SoftwareSerial mySerial(8,9);

//Miscellanous variables
int currentTime = 0; //Timer in milliseconds
int timer1 = 0; //Timer for 200hz
int timer2 = 0; //Timer for 5hz
//String gpsData;

void setup(){
 
  Serial.begin(9600);
  Wire.begin();
  SPI.begin();

  bmp085Calibration();
  initializeGPS();
  MPU6000_Init(); 
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
    timer1 = currentTime;
  }
  
  // 5Hz
  if(currentTime - timer2 >= 333)
  {
    Serial.println("GPS:  ");
    readGPS();
    timer2 = currentTime;
  }
  
  Serial.println();
  
//  if(bmpRead)
//  {
//    bmpRead = false;
//    readBMP();
//  }
//  
//  Serial.println();
//  
//  if(gpsRead)
//  {
//    gpsRead = false;
//    readGPS();
//  }
//  
  Serial.println();
    
  
//  float temperature = bmp085GetTemperature(bmp085ReadUT()); //MUST be called first
//  float pressure = bmp085GetPressure(bmp085ReadUP());
//  float atm = pressure / 101325; // "standard atmosphere"
//  float altitude = calcAltitude(pressure); //Uncompensated caculation - in Meters 
//
//  Serial.print("Temperature: ");
//  Serial.print(temperature, 2); //display 2 decimal places
//  Serial.println("deg C");
//
//  Serial.print("Pressure: ");
//  Serial.print(pressure, 0); //whole number only.
//  Serial.println(" Pa");
//
//  Serial.print("Standard Atmosphere: ");
//  Serial.println(atm, 4); //display 4 decimal places
//
//  Serial.print("Altitude: ");
//  Serial.print(altitude, 2); //display 2 decimal places
//  Serial.println(" M");
//  
//  gyro.read();
//
//  Serial.print("G ");
//  Serial.print("X: ");
//  Serial.print((int)gyro.g.x);
//  Serial.print(" Y: ");
//  Serial.print((int)gyro.g.y);
//  Serial.print(" Z: ");
//  Serial.println((int)gyro.g.z);
//  
//  compass.read();
//
//  Serial.print("A ");
//  Serial.print("X: ");
//  Serial.print((int)compass.a.x);
//  Serial.print(" Y: ");
//  Serial.print((int)compass.a.y);
//  Serial.print(" Z: ");
//  Serial.print((int)compass.a.z);
//  
//  Serial.print("\n");
//  
//  Serial.print("M ");
//  Serial.print("X: ");
//  Serial.print((int)compass.m.x);
//  Serial.print(" Y: ");
//  Serial.print((int)compass.m.y);
//  Serial.print(" Z: ");
//  Serial.println((int)compass.m.z);
//  
//  if(mySerial.available())
//	Serial.write(mySerial.read());
//  
//  Serial.println();//line break
//
//  delay(1000); //wait a second and get values again.
  
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

