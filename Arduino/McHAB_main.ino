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
#include "Bitstream.h"
#include <SoftwareSerial.h>

//Sensor orientation of Arduimu V3
int SENSOR_SIGN[] = {1,-1,-1,-1,1,1,-1,1,-1};

//BMP - Barometic Pressure Sensor
float temperature;
float pressure;
float atm; // "standard atmosphere"
float altitude; //Uncompensated caculation - in Meters 

//GPS
SoftwareSerial mySerial(8,9);
String gpsData = "";
String gpgga = "";
bool gpsDataReady = false;

//HMC5883 - Magnetometer
unsigned short mag_x;
unsigned short mag_y;
unsigned short mag_z;
int mag_offset[3];
float Heading;
float Heading_X;
float Heading_Y;

//MPU6000 - Accel, Gyro
unsigned short accelX;
unsigned short accelY;
unsigned short accelZ;
unsigned short gyroX;
unsigned short gyroY;
unsigned short gyroZ;

//Timer variable
int currentTime = 0; //Timer in milliseconds
int timer1 = 0; //Timer for 200hz
int timer2 = 0; //Timer for 5hz

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  SPI.begin();

  //bmp085Calibration();
  initializeGPS();
  MPU6000_Init(); 
  HMC5883_init();
}  

void loop()
{
  currentTime = millis();
  
  // 100Hz 
  if(currentTime - timer1 >= 10)
  {
    MPU6000_Read(accelX, accelY, accelZ, gyroX, gyroY, gyroZ);
    HMC5883_read(mag_x, mag_y, mag_z); 
    
    sendToSerial();
    
    timer1 = currentTime;
  }
  
  // 5Hz
  if(currentTime - timer2 >= 333)
  {
    readGPS(gpgga);
    timer2 = currentTime;
  }  
}

void sendToSerial()
{
  //Send accelerometer RAW x , y , z values
  sendToSerial(accelX);  
  sendToSerial(accelY);
  sendToSerial(accelZ);
  
  //Send gyroscope RAW x, y, z values
  sendToSerial(gyroX);
  sendToSerial(gyroY);
  sendToSerial(gyroZ);
  
  //Send mangetometer RAW, x, y, z values
  sendToSerial(mag_x);
  sendToSerial(mag_y);
  sendToSerial(mag_z);
  
  Serial.println();
  

    //Serial.println(temp1);
    //Serial.println(temp2);   
      
//    Serial.print(";aY:"); Serial.print(accelY); //Serial.print("  ");
//    Serial.print(";aZ:"); Serial.print(accelZ); //Serial.println("  ");
//    Serial.print(";gX:"); Serial.print(gyroX); //Serial.print("  ");
//    Serial.print(";gY:"); Serial.print(gyroY); //Serial.print("  ");
//    Serial.print(";gZ:"); Serial.print(gyroZ); //Serial.println("  ");  
//  
//    //Print out magnetometer
//    Serial.print(";mX:"); Serial.print(mag_x); //Serial.print("  ");
//    Serial.print(";mY:"); Serial.print(mag_y); //Serial.print("  ");
//    Serial.print(";mZ:"); Serial.print(mag_z); //Serial.println("  ");
    
    
    //Print out GPS if data is ready
    if(gpsDataReady)
    {
     // Serial.print(";GPS:" + gpgga);
      gpsDataReady = false;
      gpgga = "";
    }
    else
    {
      //Serial.println();
    }
//  Serial.print("Temp:");
//  Serial.print(temperature, 2); //display 2 decimal places
//  //Serial.println("deg C");
//
//  Serial.print(";Pres:");
//  Serial.print(pressure, 0); //whole number only.
//  //Serial.println(" Pa");
//
//  Serial.print(";Atm:");
//  Serial.print(atm, 4); //display 4 decimal places
//
//  Serial.print(";Alt:");
//  Serial.println(altitude, 2); //display 2 decimal places
  
}





