//Generated Date: Sun, 02 Jun 2024 06:28:31 GMT



int VR = 0;

void setup()
{
  Serial.begin(115200);


  pinMode(34, INPUT_PULLUP);
}

void loop()
{
  VR = analogRead(34);
  Serial.println(VR);
  delay(500);
}
