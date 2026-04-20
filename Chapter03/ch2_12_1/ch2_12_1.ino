//Generated Date: Mon, 17 Jun 2024 05:31:43 GMT

#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>

PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);
String myNFC_UID="";
uint8_t myNFC_UID_array[] = { 0, 0, 0, 0, 0, 0, 0 };
uint8_t myNFC_UID_Length;

String readFromNFC_UID() {
  uint8_t success;
  String cardUID="";
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, myNFC_UID_array, &myNFC_UID_Length);
  if (success) {
    for (uint8_t i=0; i < myNFC_UID_Length; i++)
    {
      cardUID+=((String(myNFC_UID_array[i], HEX).length()==1?"0":"")+String(myNFC_UID_array[i], HEX));
    }
  }
  cardUID.toUpperCase();
  return cardUID;
}

void setup()
{
  nfc.begin();
  Serial.begin(115200);

  nfc.setPassiveActivationRetries(0xFF);
  nfc.SAMConfig();
  delay(2000);
}

void loop()
{
  myNFC_UID_Length=0;
  myNFC_UID=readFromNFC_UID();
  if ((myNFC_UID!="")) {
    Serial.println(myNFC_UID);
  }
}
