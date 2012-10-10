#include "GPS.h"

//functions' bodies
void initializeGPS()
{
	mySerial.begin(4800);
}
void readGPS(String &GPSgpgga)
{
  char readValue = '\0';
  String gpggaString = "";
  
  while(mySerial.available())
  {
    readValue = mySerial.read();
    gpsData += readValue;
  }

  getGPGGA(GPSgpgga);
}

void getGPGGA(String &GPSgpgga)
{
  bool gpggaFound = false;
  
  //New reading. If new line is found, the string will be sent on the next cycle. Else, it will be wait until next cycle to be sent
  if(GPSgpgga == "")
  {
    //Iterate through the string to find the $GPGGA string
    for(int i = 0; i != gpsData.length(); ++i)
    {
      if(!gpggaFound && gpsData.charAt(i) == '$')
      {
        //Serial.print(gpsData.substring(i, i + 5));
        if(gpsData.substring(i, i + 6) == "$GPGGA")
        {  
            GPSgpgga += gpsData.charAt(i);
            gpggaFound = true;
        }
      }
      //If gpgga is found, store the string in the gpggaString until a new line or a null is found
      else if(gpggaFound)
      {
        if(gpsData.charAt(i) == '\n')
        {
          GPSgpgga += gpsData.charAt(i);
          gpsDataReady = true;
          break; //End loop
        }
        else if(gpsData.charAt(i) == '\0')
        {
          gpsDataReady = false;
          //No need to break since its the last character
        }
        else
        {
          GPSgpgga += gpsData.charAt(i);
        }
      }
    }
  }
  //Continu reading from last reading until a new line is reached
  else
  {
    for(int i = 0; i != gpsData.length(); ++i)
    {
      GPSgpgga += gpsData.charAt(i);
      if(gpsData.charAt(i) == '\n')
      {
        gpsDataReady = true;
        break; //Read until a new line is reached
      }
    }  
  }  
}
