//Generated Date: Fri, 14 Jun 2024 08:10:02 GMT

#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
  #error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;

#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);
#include <DHT.h>

int T = 0;
int H = 0;
DHT dht (15, DHT11);

void setup()
{
  Serial.begin(115200);
  delay(10);
  SerialBT.begin("ESP32 BLE");
  delay(10);

  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.enableUTF8Print();
  u8g2.setFont(u8g2_font_unifont_t_chinese1);
  dht.begin();
}

void loop()
{
  T = dht.readTemperature();
  H = dht.readHumidity();
  SerialBT.println(String((String(T)+String(",")+String(H))));
  u8g2.firstPage();
  do {
    u8g2.drawUTF8(0,14,String((String("溫度:")+String(T)+String("度"))).c_str());
    u8g2.drawUTF8(0,30,String((String("相對濕度:")+String(H)+String("%"))).c_str());
  } while ( u8g2.nextPage() );
  delay(1000);
}
