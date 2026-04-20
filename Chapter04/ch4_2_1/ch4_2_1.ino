//Generated Date: Thu, 18 Jul 2024 07:22:02 GMT

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
  digitalWrite(16, 1);

}

void ljjBtDisconnected(){
  digitalWrite(16, 0);

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
  setupBLE("ESP32_BLE");
  pinMode(16, OUTPUT);
}

void loop()
{

}
