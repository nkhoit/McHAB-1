#ifndef HMC5883_H
#define HMC5883_H

#include <math.h>
#include <Wire.h>
#include <Arduino.h>

// Local magnetic declination (in degrees)
// I use this web : http://www.ngdc.noaa.gov/geomagmodels/Declination.jsp
#define MAGNETIC_DECLINATION -6.0    // corrects magnetic bearing to true north
// Magnetometer OFFSETS (magnetometer calibration) (only for ArduIMU v3)
#define MAG_OFFSET_X 0
#define MAG_OFFSET_Y 0
#define MAG_OFFSET_Z 0

#define COMPASS_ADDRESS      0x1E
#define ConfigRegA           0x00
#define ConfigRegB           0x01
#define ModeRegister         0x02
#define DataOutputXMSB       0x03
#define DataOutputXLSB       0x04
#define DataOutputZMSB       0x05
#define DataOutputZLSB       0x06
#define DataOutputYMSB       0x07
#define DataOutputYLSB       0x08
#define StatusRegister       0x09
#define IDRegisterA          0x0A
#define IDRegisterB          0x0B
#define IDRegisterC          0x0C

// default gain value
#define magGain              0x20

// ModeRegister valid modes
#define ContinuousConversion 0x00
#define SingleConversion     0x01

// ConfigRegA valid sample averaging
#define SampleAveraging_1    0x00
#define SampleAveraging_2    0x01
#define SampleAveraging_4    0x02
#define SampleAveraging_8    0x03

// ConfigRegA valid data output rates
#define DataOutputRate_0_75HZ 0x00
#define DataOutputRate_1_5HZ  0x01
#define DataOutputRate_3HZ    0x02
#define DataOutputRate_7_5HZ  0x03
#define DataOutputRate_15HZ   0x04
#define DataOutputRate_30HZ   0x05
#define DataOutputRate_75HZ   0x06

// ConfigRegA valid measurement configuration bits
#define NormalOperation      0x10
#define PositiveBiasConfig   0x11
#define NegativeBiasConfig   0x12

#define ToRad(x) (x*0.01745329252)  // *pi/180

extern int SENSOR_SIGN[];

extern unsigned short mag_x;
extern unsigned short mag_y;
extern unsigned short mag_z;
extern int mag_offset[3];
extern float Heading;
extern float Heading_X;
extern float Heading_Y;

bool HMC5883_init();
void HMC5883_set_offset(int offsetx, int offsety, int offsetz);
void HMC5883_read(unsigned short &HMCmx, unsigned short &HMCmy, unsigned short &HMCmz);
void HMC5883_calculate(float roll, float pitch);

#endif
