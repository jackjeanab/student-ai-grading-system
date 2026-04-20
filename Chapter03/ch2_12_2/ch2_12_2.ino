//Generated Date: Mon, 17 Jun 2024 05:40:31 GMT

#include <Wire.h>
#include <PN532_I2C.h>
#include <PN532.h>
#include <NfcAdapter.h>
PN532_I2C pn532i2c(Wire);
PN532 nfc(pn532i2c);
uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
uint8_t uidLength;
uint8_t keya[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
uint8_t keyb[6] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };
String readerChip = "";
String readerVersion = "";
boolean pn532Connected = false;

String PN532_readInfo(String type) {
  if (type=="chip")
  	return readerChip;
  else if (type=="version")
  	return readerVersion;
  else if (type=="uid"||type=="uidlength") {
    boolean success;
    success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
    if (success) {
      if (type=="uidlength")
  	  return String(uidLength);
      String uidString = "";
      for (uint8_t i = 0; i < uidLength; i++) {
        uidString += String(uid[i], HEX);
      }
      return uidString;
    }
    else
      return "";
  }
  return "";
}
void PN532_writeData(int block, String text, boolean NDEF, uint8_t ndefprefix) {
  if (PN532_readInfo("uid") != "") {
  	boolean success;
  	int i = 16;
  	if (!NDEF)
  	  nfc.mifareclassic_AuthenticateBlock(uid, uidLength, block, 0, keya);
  	else {
  	  nfc.mifareclassic_AuthenticateBlock(uid, uidLength, block, 0, keyb);
  	}
  	char *data = new char[text.length() + 1];
  	strcpy(data, text.c_str());
  	Serial.println("write: "+String(data));
  	if (NDEF) {
  	  if (strlen(data) <= 38) {
          success = nfc.mifareclassic_WriteNDEFURI(1, ndefprefix, (char *)text.c_str());
          if (!success)
            Serial.println("Write data failed!");
  	  }
  	}
  	else {
        success = nfc.mifareclassic_WriteDataBlock(block, (uint8_t *)data);
        if (!success)
          Serial.println("Write data failed!");
  	}
  }
}
String PN532_readData(int block) {
  if (PN532_readInfo("uid") != "") {
    boolean success;
    nfc.mifareclassic_AuthenticateBlock(uid, uidLength, block, 0, keya);
	  int i = 16;
	  if (uidLength == 4)
	    i = 16;
    else if (uidLength == 7)
 	    i = 32;
	  uint8_t data[i];
	  if (uidLength == 4)
	    success = nfc.mifareclassic_ReadDataBlock(block, data);
	  else if (uidLength == 7)
	    success = nfc.mifareultralight_ReadPage(block, data);
	    Serial.println("read: "+String((char *)data));
	  if (success)
	    return String((char *)data);
	  else
	    return "";
  }
}
void PN532_clear_block(int sector, int block) {
  PN532_writeData((sector*4+block), "", false, 0);
}

void setup()
{
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.println("PN53x card not found!");
    pn532Connected = false;
  }
  else
    pn532Connected = true;
  readerChip = "PN5"+String(((int((versiondata>>24) & 0xFF)-int((versiondata>>24) & 0xFF)%16)*10/16)+int((versiondata>>24) & 0xFF)%16);
  readerVersion = String(((int((versiondata>>16) & 0xFF)-int((versiondata>>16) & 0xFF)%16)*10/16)+int((versiondata>>16) & 0xFF)%16)+"."+String(((int((versiondata>>8) & 0xFF)-int((versiondata>>8) & 0xFF)%16)*10/16)+int((versiondata>>8) & 0xFF)%16);
  nfc.setPassiveActivationRetries(0xFF);
  nfc.SAMConfig();

  Serial.begin(115200);

  delay(2000);
}

void loop()
{
  if (pn532Connected) {
    Serial.println((PN532_readInfo("uid")));
  }
}
