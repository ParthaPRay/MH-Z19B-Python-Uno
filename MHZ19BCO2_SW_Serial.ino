// Partha Pratim Ray
// Date August 21, 2023


#include "SoftwareSerial.h"
#include "Arduino.h"
#include "MHZCO2.h"


const int TX = 10;
const int RX = 11;

SoftwareSerial MHZ(TX, RX);


MHZ19B MHZ19B;

int count = 0; // To count the loop

void setup()
{
  Serial.begin(115200);
  Serial.println(__FILE__);
  Serial.print("MHZCO2_LIB_VERSION: ");
  Serial.println(MHZCO2_LIB_VERSION);
  
  MHZ19B.begin(&MHZ);
  MHZ.begin(115200);
}


void loop()
{
  MHZ19B.measure();
  
  count++;
  if (count>5){       // First two data from MH-Z19B are not stable 
  Serial.print("CO2:  ");  // So, for sake of more bravety, first 5 values are ignored and later on the data sent to Serial
  Serial.println(MHZ19B.getCO2());
  }

  delay(1000);
}
