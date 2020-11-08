#include "Adafruit_CCS811.h"
#include <Arduino.h>

Adafruit_CCS811 ccs;

void setup() {
  Serial.begin(9600);
  if(!ccs.begin()){
    Serial.println("Failed to start sensor CO2! Please check your wiring.");
    while(1);
  }

  // Wait for the sensor to be ready
  while(!ccs.available());
}

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int nPin = getValue(data, ',', 0).toInt();
    int value = getValue(data, ',', 1).toInt();
    digitalWrite(nPin, value);
    Serial.println(data);
    Serial.flush();
  }
  if(ccs.available()){
    if(!ccs.readData()){
      String data = String(ccs.geteCO2()) + "," + String(ccs.getTVOC());
      Serial.println(data);
    }
    else{
      Serial.println("None");
      while(1);
    }
  }
  delay(1500);
}