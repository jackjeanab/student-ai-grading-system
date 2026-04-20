//Generated Date: Sun, 02 Jun 2024 06:38:38 GMT



int Light = 0;

void setup()
{
  Serial.begin(115200);


  pinMode(39, INPUT_PULLUP);
}

void loop()
{
  Light = analogRead(39);
  Serial.println(Light);
  delay(200);
}
