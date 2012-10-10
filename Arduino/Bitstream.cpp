#include "Bitstream.h"

void sendToSerial(unsigned short value)
{
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value);
}

void sendToSerial(short value)
{
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value);
}

void sendToSerial(unsigned long value)
{
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value);  
}

void sendToSerial(long value)
{
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value & 0xff);
  value = value >> 8;
  Serial.write(value);  
}

