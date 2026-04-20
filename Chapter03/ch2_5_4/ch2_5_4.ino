//Generated Date: Thu, 06 Jun 2024 08:54:00 GMT

#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void setup()
{
  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.disableUTF8Print();
  u8g2.setFont(u8g2_font_6x12_t_symbols);
  u8g2.firstPage();
  do {
    u8g2.drawGlyph(0,14,9680);
  } while ( u8g2.nextPage() );
}

void loop()
{

}
