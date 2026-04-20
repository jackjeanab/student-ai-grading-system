//Generated Date: Wed, 12 Jun 2024 12:45:23 GMT

#include <Ultrasonic.h>

Ultrasonic ultrasonic0(12, 16);

void setup()
{
  Serial.begin(115200);


}

void loop()
{
  Serial.println(ultrasonic0.convert(ultrasonic0.timing(), 1));
  delay(200);
}
