//Generated Date: Thu, 09 May 2024 13:30:15 GMT



void setup()
{

}

void loop()
{
  pinMode(16, OUTPUT);
  digitalWrite(16, HIGH);
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  delay(1000);
  pinMode(16, OUTPUT);
  digitalWrite(16, LOW);
  pinMode(12, OUTPUT);
  digitalWrite(12, LOW);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  delay(1000);
}
