//Generated Date: Tue, 23 Jul 2024 07:47:38 GMT

String RX_String = "";
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

BLECharacteristic *pCharacteristic;
bool btConnected = false;
bool btReceiveDone=false;
String btRxLoad="";
String sendTemp="";

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

  setupBLE("ESP32_BLE");
  pinMode(25, OUTPUT);
}

void loop()
{
  if (btConnected && btReceiveDone && btRxLoad.length()>0){
    RX_String = btRxLoad;
    Serial.println(RX_String);
    if (RX_String == "ON") {
      digitalWrite(25, 1);
    } else if (RX_String == "OFF") {
      digitalWrite(25, 0);
    }
    btRxLoad="";
  }
}
