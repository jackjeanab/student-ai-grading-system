//Generated Date: Wed, 26 Jun 2024 01:56:24 GMT



void setup()
{

  pinMode(5, INPUT_PULLUP);
}

void loop()
{
  if ((digitalRead(5)) == 0) {
    pinMode(16, OUTPUT);
    digitalWrite(16, HIGH);
  } else {
    pinMode(16, OUTPUT);
    digitalWrite(16, LOW);
  }
}
