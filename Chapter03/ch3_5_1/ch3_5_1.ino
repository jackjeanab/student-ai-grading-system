//Generated Date: Tue, 09 Jul 2024 06:48:01 GMT

#include <IRremote.hpp>
#define MY_IR_RECEIVE_PIN 33
decode_results results;
String myCodeType;
String myIRcode;

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


}

void loop()
{
  if (IrReceiver.decode(&results)) {
    if (results.decode_type>0){
      myCodeType=ir_type(results.decode_type);
      if (String(results.value, HEX)!="ffffffff"){
        myIRcode=String(results.value, HEX);
        Serial.println((String("訊息類型：")+String(myCodeType)));
        Serial.println((String("訊息：")+String(myIRcode)));
      }
    }
    IrReceiver.resume();
  }
}
