//Generated Date: Tue, 04 Jun 2024 06:40:07 GMT

#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup()
{
  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.enableUTF8Print();
  u8g2.setFont(u8g2_font_unifont_t_chinese1);
  u8g2.firstPage();
  do {
    u8g2.drawUTF8(0,14,String("嗨，世界！").c_str());
  } while ( u8g2.nextPage() );
}

void loop()
{

}
