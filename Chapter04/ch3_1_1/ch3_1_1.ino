//Generated Date: Wed, 12 Jun 2024 12:19:38 GMT

#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
  #error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;

String ESP32Ble = "";

void setup()
{
  Serial.begin(115200);
  delay(10);
  SerialBT.begin("ESP32 BLE");
  delay(10);


  pinMode(16, OUTPUT);
}

void loop()
{
  if (SerialBT.available()) {
    String BluetoothData = "";
    while (SerialBT.available()) {
      char c=SerialBT.read();
      BluetoothData=BluetoothData+String(c);
      delay(1);
    }
    ESP32Ble = BluetoothData;
    Serial.println(ESP32Ble);
    if (ESP32Ble == "1") {
      digitalWrite(16, 1);
    } else if (ESP32Ble == "2") {
      digitalWrite(16, 0);
    }
  }
}
