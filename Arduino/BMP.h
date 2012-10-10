#ifndef BMP_h
#define BMP_h
#define BMP085_ADDRESS 0x77

#include <Wire.h>
#include <Arduino.h>

//Variables declaration
extern const unsigned char OSS; 
extern int ac1;
extern int ac2;
extern int ac3;
extern unsigned int ac4;
extern unsigned int ac5;
extern unsigned int ac6;
extern int b1;
extern int b2;
extern int mb;
extern int mc;
extern int md;
extern long b5;

//class declaration
void bmp085Calibration();
float bmp085GetTemperature(unsigned int ut);
long bmp085GetPressure(unsigned long up);
char bmp085Read(unsigned char address);
int bmp085ReadInt(unsigned char address);
unsigned int bmp085ReadUT();
unsigned long bmp085ReadUP();
float calcAltitude(float pressure);
void readBMP(float &BMPtemperature, float &BMPpressure, float &BMPatm, float &BMPaltitude); 


#endif
