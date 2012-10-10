#include "HMC5883.h"

//int mag_x;
//int mag_y;
//int mag_z;
//int mag_offset[3];
//float Heading;
//float Heading_X;
//float Heading_Y;

bool HMC5883_init()
{
  int success = 0;
  uint8_t aux_byte;

  Wire.begin();
  delay(10);

  //mag_offset[0] = 0;
  //mag_offset[1] = 0;
  //mag_offset[2] = 0;

  Wire.beginTransmission(COMPASS_ADDRESS);
  Wire.write((uint8_t)ConfigRegA);
  aux_byte = (SampleAveraging_8<<5 | DataOutputRate_75HZ<<2 | NormalOperation);
  Wire.write(aux_byte);
  Wire.endTransmission();
  delay(50);

  Wire.beginTransmission(COMPASS_ADDRESS);
  Wire.write((uint8_t)ModeRegister);
  Wire.write((uint8_t)ContinuousConversion);        // Set continuous mode (default to 10Hz)
  Wire.endTransmission();                 // End transmission
  delay(50);
  
  return(1);
}

// set mag offsets
void HMC5883_set_offset(int offsetx, int offsety, int offsetz)
{
  mag_offset[0] = offsetx;
  mag_offset[1] = offsety;
  mag_offset[2] = offsetz;
}

// Read Sensor data in chip axis
void HMC5883_read(unsigned short &HMCmx, unsigned short &HMCmy, unsigned short &HMCmz)
{
  int i = 0;
  byte buff[6];

  Wire.beginTransmission(COMPASS_ADDRESS);
  Wire.write(0x03);        //sends address to read from
  Wire.endTransmission(); //end transmission

    //Wire.beginTransmission(COMPASS_ADDRESS);
  Wire.requestFrom(COMPASS_ADDRESS, 6);    // request 6 bytes from device
  while(Wire.available())
  {
    buff[i] = Wire.read();  // receive one byte
    i++;
  }
  Wire.endTransmission(); //end transmission

  if (i==6){  // All bytes received?
    // MSB byte first, then LSB
    mag_x = ((((int)buff[0]) << 8) | buff[1])*SENSOR_SIGN[6] + mag_offset[0];    // X axis
    mag_y = ((((int)buff[4]) << 8) | buff[5])*SENSOR_SIGN[7] + mag_offset[1];    // Y axis
    mag_z = ((((int)buff[2]) << 8) | buff[3])*SENSOR_SIGN[8] + mag_offset[2];    // Z axis
  }
}

void HMC5883_calculate(float roll, float pitch)
{
  float Head_X;
  float Head_Y;
  float cos_roll;
  float sin_roll;
  float cos_pitch;
  float sin_pitch;
  
  cos_roll = cos(roll);
  sin_roll = sin(roll);
  cos_pitch = cos(pitch);
  sin_pitch = sin(pitch);
  
  // Tilt compensated Magnetic field X component:
  Head_X = mag_x*cos_pitch+mag_y*sin_roll*sin_pitch+mag_z*cos_roll*sin_pitch;
  // Tilt compensated Magnetic field Y component:
  Head_Y = mag_y*cos_roll-mag_z*sin_roll;
  // Magnetic Heading
  Heading = atan2(-Head_Y,Head_X);
  
  // Declination correction (if supplied)
  if( MAGNETIC_DECLINATION != 0 ) 
  {
      Heading = Heading + ToRad(MAGNETIC_DECLINATION);
      if (Heading > M_PI)    // Angle normalization (-180 deg, 180 deg)
          Heading -= (2.0 * M_PI);
      else if (Heading < -M_PI)
          Heading += (2.0 * M_PI);
  }
	
  // Optimization for external DCM use. Calculate normalized components
  Heading_X = cos(Heading);
  Heading_Y = sin(Heading);
}
