#include "GPS.h"

//Variable declaration

SoftwareSerial mySerial(8,9);
String gpsData;
String gpgga = "";
bool dataReady = false;

//functions' bodies
void initializeGPS(){
	mySerial.begin(4800);
}
void readGPS()
{
  char readValue = '\0';
  String gpggaString = "";
  gpsData = "";
  
  while(mySerial.available())
  {
    readValue = mySerial.read();
    gpsData += readValue;
  }
  
 // Serial.print(gpsData);  
  getGPGGA();
  
  if(dataReady)
  {
    dataReady = false;
    Serial.print(gpgga);
    gpgga = "";
  }
}

void getGPGGA()
{
  bool gpggaFound = false;
  
  //New reading. If new line is found, the string will be sent on the next cycle. Else, it will be wait until next cycle to be sent
  if(gpgga == "")
  {
    //Iterate through the string to find the $GPGGA string
    for(int i = 0; i != gpsData.length(); ++i)
    {
      if(!gpggaFound && gpsData.charAt(i) == '$')
      {
        //Serial.print(gpsData.substring(i, i + 5));
        if(gpsData.substring(i, i + 6) == "$GPGGA")
        {  
            gpgga += gpsData.charAt(i);
            gpggaFound = true;
        }
      }
      //If gpgga is found, store the string in the gpggaString until a new line or a null is found
      else if(gpggaFound)
      {
        if(gpsData.charAt(i) == '\n')
        {
          gpgga += gpsData.charAt(i);
          dataReady = true;
          break; //End loop
        }
        else if(gpsData.charAt(i) == '\0')
        {
          dataReady = false;
          //No need to break since its the last character
        }
        else
        {
          gpgga += gpsData.charAt(i);
        }
      }
    }
  }
  //Continu reading from last reading until a new line is reached
  else
  {
    Serial.print("aaa");
    for(int i = 0; i != gpsData.length(); ++i)
    {
      gpgga += gpsData.charAt(i);
      if(gpsData.charAt(i) == '\n')
      {
        dataReady = true;
        break; //Read until a new line is reached
      }
    }  
  }  
}
