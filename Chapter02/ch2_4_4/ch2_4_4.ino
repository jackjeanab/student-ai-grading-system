//Generated Date: Sun, 30 Jun 2024 08:32:16 GMT

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
  if (Light < 300) {
    pinMode(16, OUTPUT);
    digitalWrite(16, HIGH);
  } else {
    pinMode(16, OUTPUT);
    digitalWrite(16, LOW);
  }
}
