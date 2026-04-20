//Generated Date: Fri, 07 Jun 2024 11:01:41 GMT

#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup()
{
  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.enableUTF8Print();
  u8g2.setFont(u8g2_font_unifont_t_chinese1);
  u8g2.clear();
  u8g2.firstPage();
  do {
    u8g2.drawUTF8(0,14,String("溫度：").c_str());
    u8g2.drawUTF8(0,32,String("相對濕度：").c_str());
  } while ( u8g2.nextPage() );
}

void loop()
{

}
