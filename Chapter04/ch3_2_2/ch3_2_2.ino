//Generated Date: Fri, 14 Jun 2024 08:58:00 GMT

#include <BleKeyboard.h>
BleKeyboard bleKeyboard;

void blekeyboard(String type, uint8_t keycode1, uint8_t keycode2, uint8_t keycode3, int presstime, String characters) {
  if(bleKeyboard.isConnected()) {
    if (type=="press") {
      if (keycode1!=-1) bleKeyboard.press(keycode1);
      if (keycode2!=-1) bleKeyboard.press(keycode2);
      if (keycode3!=-1) bleKeyboard.press(keycode3);
      delay(presstime);
      bleKeyboard.releaseAll();
    } else if (type=="press_norelease") {
      if (keycode1!=-1) bleKeyboard.press(keycode1);
    } else if (type=="release") {
      if (keycode1!=-1) bleKeyboard.release(keycode1);
    } else if (type=="release_all") {
      bleKeyboard.releaseAll();
    } else if (type=="print") {
      bleKeyboard.print(characters);
    } else if (type=="write") {
      bleKeyboard.write(char(keycode1));
    }
  }
}

void setup()
{
  bleKeyboard.setName("ESP32 BLE Keyboard");
  bleKeyboard.begin();
  delay(10);


  pinMode(5, INPUT_PULLUP);
  pinMode(36, INPUT_PULLUP);
}

void loop()
{
  if (digitalRead(5)==0) {
    blekeyboard("press", (KEY_LEFT_CTRL), (99), -1, 100, "");
  } else if (digitalRead(36)==0) {
    blekeyboard("press", (KEY_LEFT_CTRL), (118), -1, 100, "");
  }
  delay(100);
}
