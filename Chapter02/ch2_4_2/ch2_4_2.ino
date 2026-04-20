//Generated Date: Sat, 29 Jun 2024 10:15:09 GMT

int VR = 0;
int VR2LED = 0;

void setup()
{
  Serial.begin(115200);


  pinMode(34, INPUT_PULLUP);
  ledcSetup(1, 5000, 8);
  ledcAttachPin(16, 1);
}

void loop()
{
  VR = analogRead(34);
  VR2LED = map(VR,0,4095,0,255);
  ledcWrite(1, VR2LED);
  Serial.println(VR2LED);
}
