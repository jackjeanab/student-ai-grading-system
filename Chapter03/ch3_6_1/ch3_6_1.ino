//Generated Date: Mon, 15 Jul 2024 08:30:06 GMT



void setup()
{
  Serial.begin(115200);


}

void loop()
{
  pinMode(25, OUTPUT);
  digitalWrite(25, 1);
  Serial.println("輸出高電位");
  delay(1000);
  pinMode(25, OUTPUT);
  digitalWrite(25, 0);
  Serial.println("輸出低電位");
  delay(1000);
}
