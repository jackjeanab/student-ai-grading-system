//Generated Date: Sun, 28 Jul 2024 02:14:06 GMT

int T = 0;
int H = 0;
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include "SimpleDHT.h"
SimpleDHT11 dht11(15);
byte dht11_temperature = 0;
byte dht11_humidity = 0;
#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

BLECharacteristic *pCharacteristic;
bool btConnected = false;
bool btReceiveDone=false;
String btRxLoad="";
String sendTemp="";

void dht11_read() {
  dht11_temperature = 0;
  dht11_humidity = 0;
  dht11.read(&dht11_temperature, &dht11_humidity, NULL);
}

void Display(int T4F, int H4F) {
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.firstPage();
  do {
    u8g2.drawStr(0,14,String((String("T:")+String(T4F))).c_str());
    u8g2.drawStr(0,30,String((String("H:")+String(H4F))).c_str());
  } while ( u8g2.nextPage() );
}

void ljjBtConnected(){
  pinMode(2, OUTPUT);
  digitalWrite(2, 1);

}

void ljjBtDisconnected(){
  pinMode(2, OUTPUT);
  digitalWrite(2, 0);

}

class btLjjServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      btConnected = true;
      ljjBtConnected();
    };
    void onDisconnect(BLEServer* pServer) {
      btConnected = false;
      ljjBtDisconnected();
    }
};

class btLjjCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      btReceiveDone=false;
      std::string rxValue = pCharacteristic->getValue();
      if (rxValue.length() > 0) {
        btRxLoad="";
        for (int i = 0; i < rxValue.length(); i++){
          btRxLoad +=(char)rxValue[i];
        }
        btRxLoad.replace("\r","");
        btRxLoad.replace("\n","");
        btReceiveDone=true;
      }
    }
};

void setupBLE(String BLEName){
  const char *ble_name=BLEName.c_str();
  BLEDevice::init(ble_name);
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new btLjjServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic= pService->createCharacteristic(CHARACTERISTIC_UUID_TX,BLECharacteristic::PROPERTY_NOTIFY);
  pCharacteristic->addDescriptor(new BLE2902());
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID_RX,BLECharacteristic::PROPERTY_WRITE);
  pCharacteristic->setCallbacks(new btLjjCallbacks());
  pService->start();
  pServer->getAdvertising()->addServiceUUID(SERVICE_UUID);
  pServer->getAdvertising()->setScanResponse(true);
  pServer->getAdvertising()->setMinPreferred(0x06);
  pServer->getAdvertising()->setMinPreferred(0x12);
  pServer->getAdvertising()->start();
}

void setup()
{
  Serial.begin(115200);

  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.disableUTF8Print();
  setupBLE("ESP32_BLE");
}

void loop()
{
  dht11_read();
  T = dht11_temperature;
  H = dht11_humidity;
  Display(T, H);
  sendTemp=String((String(T)+String(",")+String(H)));
  pCharacteristic->setValue(sendTemp.c_str());
  pCharacteristic->notify();
  delay(1000);
}
