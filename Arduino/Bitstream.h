#ifndef BITSTREAM_H
#define BITSTREAM_H

#include <Wire.h>
#include <Arduino.h>

void sendToSerial(unsigned short value);
void sendToSerial(short value);
void sendTOSerial(unsigned long value);
void sendToSerial(long value);

#endif
