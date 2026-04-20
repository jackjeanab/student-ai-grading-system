//Generated Date: Tue, 09 Jul 2024 02:17:23 GMT

int T = 0;
int H = 0;
#include "SimpleDHT.h"
SimpleDHT11 dht11(15);
byte dht11_temperature = 0;
byte dht11_humidity = 0;
#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void dht11_read() {
  dht11_temperature = 0;
  dht11_humidity = 0;
  dht11.read(&dht11_temperature, &dht11_humidity, NULL);
}

void Display(int T4F, int H4F) {
  u8g2.setFont(u8g2_font_unifont_t_chinese1);
  u8g2.firstPage();
  do {
    u8g2.drawUTF8(0,14,String((String("溫度：")+String(T4F)+String("度"))).c_str());
    u8g2.drawUTF8(0,32,String((String("相對濕度：")+String(H4F)+String("%"))).c_str());
  } while ( u8g2.nextPage() );
}

void setup()
{
  Serial.begin(115200);

  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.enableUTF8Print();

}

void loop()
{
  dht11_read();
  T = dht11_temperature;
  H = dht11_humidity;
  Serial.println((String("溫度：")+String(T)));
  Serial.println((String("相對濕度：")+String(H)));
  Display(T, H);
  delay(1000);
}
