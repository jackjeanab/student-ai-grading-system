//Generated Date: Wed, 26 Jun 2024 01:53:25 GMT



void setup()
{
  Serial.begin(115200);


  pinMode(5, INPUT_PULLUP);
}

void loop()
{
  Serial.println((digitalRead(5)));
  delay(100);
}
