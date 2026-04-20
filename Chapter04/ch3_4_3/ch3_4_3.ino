//Generated Date: Thu, 18 Jul 2024 09:14:34 GMT

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

byte A_Pin=5;
byte B_Pin=36;
char myBtnStatus;
bool buttonPressed(char btnName)
{
  if (btnName=='A'){
    if (digitalRead(A_Pin) == 1)
      return false;
    else
      return true;
  }
  else if (btnName=='B'){
    if (digitalRead(B_Pin) == 1)
      return false;
    else
      return true;
  } else {
    if ((digitalRead(A_Pin) == 1) && (digitalRead(B_Pin) == 1))
      return false;
    else
      return true;
  }
}

char getBtnStatus(){
  char buttonStatus=' ';
  int checkButtonDelay=200;
  if (buttonPressed('A')){
    delay(checkButtonDelay);
    if (buttonPressed('A')){
      buttonStatus='A';
      if (buttonPressed('B'))
        buttonStatus='C';
    }
  } else if (buttonPressed('B')){
      delay(checkButtonDelay);
      if (buttonPressed('B')){
        buttonStatus='B';
        if (buttonPressed('A'))
          buttonStatus='C';
      }
  }
  return buttonStatus;
}

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
  Serial.begin(115200);

  setupBLE("ESP32_BLE");
  pinMode(A_Pin, INPUT);
  pinMode(B_Pin, INPUT);
  pinMode(16, OUTPUT);
}

void loop()
{
  myBtnStatus=getBtnStatus();
  if (myBtnStatus=='A'){
    sendTemp=String((String(random(0, 100))+String(",")+String(random(0, 100))));
    pCharacteristic->setValue(sendTemp.c_str());
    pCharacteristic->notify();
    while(buttonPressed('A')){}
  }
}
