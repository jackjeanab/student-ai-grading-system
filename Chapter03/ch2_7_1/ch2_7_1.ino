//Generated Date: Thu, 06 Jun 2024 21:53:38 GMT

#include "SimpleDHT.h"
SimpleDHT11 dht11(15);
byte dht11_temperature = 0;
byte dht11_humidity = 0;

void dht11_read() {
  dht11_temperature = 0;
  dht11_humidity = 0;
  dht11.read(&dht11_temperature, &dht11_humidity, NULL);
}

void setup()
{
  Serial.begin(115200);


}

void loop()
{
  dht11_read();
  Serial.println((String("溫度：")+String(dht11_temperature)));
  Serial.println((String("相對濕度：")+String(dht11_humidity)));
  delay(1000);
}
