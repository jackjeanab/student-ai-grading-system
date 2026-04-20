//Generated Date: Wed, 26 Jun 2024 06:06:43 GMT



void setup()
{

  ledcSetup(1, 5000, 8);
  ledcAttachPin(16, 1);
}

void loop()
{
  ledcWrite(1, 0);
  delay(1000);
  ledcWrite(1, 127);
  delay(1000);
  ledcWrite(1, 255);
  delay(1000);
}
