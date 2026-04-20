//Generated Date: Mon, 17 Jun 2024 02:08:45 GMT

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified(87844);
sensors_event_t event;

void setup()
{
  Serial.begin(115200);


  if(!accel.begin()) {
    Serial.println("Ooops, no ADXL345 detected ... Check your wiring!");
  }
  accel.setRange(ADXL345_RANGE_16_G);
}

void loop()
{
  accel.getEvent(&event);
  Serial.print((String("X軸: ")+String(event.acceleration.x)+String("   ")));
  Serial.print((String("Y軸: ")+String(event.acceleration.y)+String("   ")));
  Serial.println((String("Z軸: ")+String(event.acceleration.z)));
  delay(100);
}
