//Generated Date: Wed, 03 Jul 2024 11:46:50 GMT



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

void setup()
{
  pixels.begin();
  pixels.show();

  pixels.setBrightness(100);
  MatrixLedAll("000000");
  MatrixLedOne((1-1),"ff0000");
  MatrixLedOne((2-1),"000099");
  MatrixLedOne((3-1),"009900");
}

void loop()
{

}
