#include "Adafruit_CCS811.h"
#include <Arduino.h>
#include "DHT.h"
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define DHTTYPE DHT22
#define DHTPIN 7
#define LIGHT_PIN 5
#define WATER_TEMP_PIN 4

OneWire oneWire(WATER_TEMP_PIN);
DallasTemperature water_temp(&oneWire);
Adafruit_CCS811 ccs;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  if(!ccs.begin()){
    Serial.println("Failed to start sensor CO2! Please check your wiring.");
    while(1);
  }
  pinMode(LIGHT_PIN,INPUT);
  dht.begin();
  water_temp.begin();
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

void getSensorValue(){
  String sensor_data = "";
  if(ccs.available()){
    if(!ccs.readData()){
      sensor_data += String(ccs.geteCO2()) + "," + String(ccs.getTVOC());
    }
  }
  sensor_data += String("," + String(dht.readHumidity()) + "," + String(dht.readTemperature()) + "," + String(digitalRead(LIGHT_PIN)) + ",");
  water_temp.requestTemperatures();
  sensor_data += String(water_temp.getTempCByIndex(0));
  Serial.println(sensor_data);
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
  getSensorValue();
  delay(1500);
}