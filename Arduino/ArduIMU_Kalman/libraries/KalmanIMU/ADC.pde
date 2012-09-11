void read_adc_raw(void)
{
  MPU6000_Read();    // Read MPU6000 sensor values
  AN[0] = gyroX;   
  AN[1] = gyroY;
  AN[2] = gyroZ;
  AN[3] = accelX;
  AN[4] = accelY;
  AN[5] = accelZ;  

}

int read_adc(int select)
{
  return (AN[select]-AN_OFFSET[select])*SENSOR_SIGN[select];
}

void printdata(void)
{     
      Serial.print("!!!");
      
      #if PRINT_ANALOGS == 1
      Serial.print("AN0:");
      Serial.print(read_adc(0));
      Serial.print(";AN1:");
      Serial.print(read_adc(1));
      Serial.print(";AN2:");
      Serial.print(read_adc(2));  
      Serial.print(";AN3:");
      Serial.print(read_adc(3));
      Serial.print (";AN4:");
      Serial.print(read_adc(4));
      Serial.print (";AN5:");
      Serial.print(read_adc(5));
      Serial.print (";");
      #endif
      
      #if PRINT_KALMAN == 1
      Serial.print("ANX:");
      Serial.print(ToDeg(xkaldata.angle));
      Serial.print(";ANY:");
      Serial.print(ToDeg(ykaldata.angle));
      Serial.print(";RTX:");
      Serial.print(ToDeg(xkaldata.rate));
      Serial.print(";RTY:");
      Serial.print(ToDeg(ykaldata.rate));
      Serial.print(";BSX:");
      Serial.print(ToDeg(xkaldata.q_bias));
      Serial.print(";BSY:");
      Serial.print(ToDeg(ykaldata.q_bias));
      Serial.print (";");
      #endif
      
      #if PROCESS_GPS == 1
      #if PRINT_GPS == 1
      Serial.print("LAT:");
      Serial.print((long)(lat*10000000));
      Serial.print(";LON:");
      Serial.print((long)(lon*10000000));
      Serial.print(";ALT:");
      Serial.print(alt_MSL);
      Serial.print(";COG:");
      Serial.print((ground_course));
      Serial.print(";SOG:");
      Serial.print(ground_speed);
      Serial.print(";FIX:");
      Serial.print((int)gpsFix);
      Serial.print (";");
      #endif
      #endif
      
      Serial.println("***"); 
}

long convert_to_dec(float x)
{
  return x*1000000;
}
//Activating the ADC interrupts. 
void Analog_Init(void)
{
 ADCSRA|=(1<<ADIE)|(1<<ADEN);
 ADCSRA|= (1<<ADSC);
}

int Analog_Read(uint8_t pin)
{
  return analog_buffer[pin];
}

void Analog_Reference(uint8_t mode)
{
	analog_reference = mode;
}
//ADC interrupt vector, this piece of
//is executed everytime a convertion is done. 
ISR(ADC_vect)
{
  volatile uint8_t low, high;
  low = ADCL;
  high = ADCH;
  analog_buffer[MuxSel]=(high << 8) | low;
  MuxSel++;
  if(MuxSel >=8) MuxSel=0;
  ADMUX = (analog_reference << 6) | (MuxSel & 0x07);
  // start the conversion
  ADCSRA|= (1<<ADSC);
}
