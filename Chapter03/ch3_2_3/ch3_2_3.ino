//Generated Date: Mon, 01 Jul 2024 06:35:05 GMT



String matrixString = "000000000000000000";

int MatrixLed_marquee_time = 500;

int MatrixLed_marquee_rotate = 0;

int MatrixLed_leds_number = 3;

#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(3, 26, NEO_GRB + NEO_KHZ800);

String strTemp_ = "";

int HextoRGB(char val) {
  String hex ="0123456789abcdef";
  return hex.indexOf(val);
}

void MatrixLedAll(String color) {
  color.replace("#","");
  for(int i=0;i<(matrixString.length()/6);i++) {
    matrixString[i*6+0] = color[0];
    matrixString[i*6+1] = color[1];
    matrixString[i*6+2] = color[2];
    matrixString[i*6+3] = color[3];
    matrixString[i*6+4] = color[4];
    matrixString[i*6+5] = color[5];
    uint32_t R,G,B;
    R = (HextoRGB(color[0])*16+HextoRGB(color[1]));
    G = (HextoRGB(color[2])*16+HextoRGB(color[3]));
    B = (HextoRGB(color[4])*16+HextoRGB(color[5]));
    pixels.setPixelColor(i, pixels.Color(R, G, B));
  }
  pixels.show();
}

void MatrixLedOne(int i, String color) {
  color.replace("#","");
  matrixString[i*6+0] = color[0];
  matrixString[i*6+1] = color[1];
  matrixString[i*6+2] = color[2];
  matrixString[i*6+3] = color[3];
  matrixString[i*6+4] = color[4];
  matrixString[i*6+5] = color[5];
  uint32_t R,G,B;
  R = (HextoRGB(color[0])*16+HextoRGB(color[1]));
  G = (HextoRGB(color[2])*16+HextoRGB(color[3]));
  B = (HextoRGB(color[4])*16+HextoRGB(color[5]));
  pixels.setPixelColor(i, pixels.Color(R, G, B));
  pixels.show();
}

String HexReverse_s(int val, int pos) {
  int i = 0;
  String s = "0123456789abcdef";
  if (pos==1)
    i = (val-val%16)/16;
  else if (pos==2)
    i = val%16;
  return String(s[i]);
}

void setup()
{
  pixels.begin();
  pixels.show();

  pixels.setBrightness(100);
  MatrixLedAll("000000");
}

void loop()
{
  for (int i = 1; i <= 3; i++) {
    strTemp_ = HexReverse_s(255, 1)+HexReverse_s(255, 2)+HexReverse_s(0, 1)+HexReverse_s(0, 2)+HexReverse_s(0, 1)+HexReverse_s(0, 2);
    MatrixLedOne((i-1), strTemp_);
    delay(1000);
  }
  for (int i = 1; i <= 3; i++) {
    strTemp_ = HexReverse_s(0, 1)+HexReverse_s(0, 2)+HexReverse_s(255, 1)+HexReverse_s(255, 2)+HexReverse_s(0, 1)+HexReverse_s(0, 2);
    MatrixLedOne((i-1), strTemp_);
    delay(1000);
  }
  for (int i = 1; i <= 3; i++) {
    strTemp_ = HexReverse_s(0, 1)+HexReverse_s(0, 2)+HexReverse_s(0, 1)+HexReverse_s(0, 2)+HexReverse_s(255, 1)+HexReverse_s(255, 2);
    MatrixLedOne((i-1), strTemp_);
    delay(1000);
  }
}
