//Generated Date: Sun, 02 Jun 2024 03:28:54 GMT



void setup()
{
  Serial.begin(115200);


  ledcSetup(1, 5000, 8);
  ledcAttachPin(16, 1);
}

void loop()
{
  for (int i = 0; i <= 255; i += 5) {
    Serial.println((String("i = ")+String(i)));
    ledcWrite(1, i);
    delay(200);
  }
}
