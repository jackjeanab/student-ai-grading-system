//Generated Date: Wed, 10 Jul 2024 08:27:49 GMT

String ReData = "";
#include <IRremote.hpp>
#define MY_IR_RECEIVE_PIN 33
decode_results results;
String myCodeType;
String myIRcode;
#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

void Display(String Text, int Dir) {
  u8g2.firstPage();
  do {
    u8g2.setFont(u8g2_font_unifont_t_chinese1);
    u8g2.drawUTF8(3,18,String(Text).c_str());
    u8g2.setFont(u8g2_font_open_iconic_all_2x_t);
    u8g2.drawGlyph(55,20,Dir);
  } while ( u8g2.nextPage() );
}

String ir_type(int tip)
{
  if (tip == 14){
    return "RC5";
  } else if (tip == 15){
    return "RC6";
  } else if (tip == 7){
    return "NEC";
  } else if (tip == 18){
    return "SONY";
  } else if (tip == 8){
    return "PANASONIC";
  } else if (tip == 4){
    return "JVC";
  } else if (tip == 16){
    return "SAMSUNG";
  } else if (tip == 5){
    return "LG";
  } else if (tip == 3){
    return "SHARP";
  } else if (tip == 22){
    return "LEGO_PF";
  } else {
    return String(tip);
  }
}

void setup()
{
  Serial.begin(115200);

  IrReceiver.begin(MY_IR_RECEIVE_PIN);

  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.enableUTF8Print();
  Display("未啟動", 113);
}

void loop()
{
  if (IrReceiver.decode(&results)) {
    if (results.decode_type>0){
      myCodeType=ir_type(results.decode_type);
      if (String(results.value, HEX)!="ffffffff"){
        myIRcode=String(results.value, HEX);
        ReData = myIRcode;
        Serial.println((String("訊息：")+String(ReData)));
        if (ReData == "ff38c7") {
          Display("停車歐", 121);
        } else if (ReData == "ff18e7") {
          Display("往前進", 76);
        } else if (ReData == "ff4ab5") {
          Display("倒車啦", 73);
        } else if (ReData == "ff10ef") {
          Display("左轉轉", 74);
        } else if (ReData == "ff5aa5") {
          Display("右轉轉", 75);
        }
      }
    }
    IrReceiver.resume();
  }
}
