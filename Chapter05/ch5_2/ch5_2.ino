//Generated Date: Thu, 01 Aug 2024 08:27:33 GMT

String Date = "";
String Time = "";
#include <WiFi.h>
#include <time.h>
#include <U8g2lib.h>
#include <Wire.h>
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

char _lwifi_ssid[] = "你的WiFi熱點帳號";
char _lwifi_pass[] = "你的WiFi熱點帳號";
void Display(String Date4F, String Time4F) {
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.firstPage();
  do {
    u8g2.drawStr(0,14,String(Date4F).c_str());
    u8g2.drawStr(0,30,String(Time4F).c_str());
  } while ( u8g2.nextPage() );
}

int get_data_from_RTC(byte dataType) {
  int myResult=0;
  time_t t = time(NULL);
  struct tm *t_st;
  t_st = localtime(&t);
  switch(dataType){
    case 0:
      myResult=(1900 + t_st->tm_year);
      break;
    case 1:
      myResult=( 1 + t_st->tm_mon);
      break;
    case 2:
      myResult=t_st->tm_mday;
      break;
    case 3:
      myResult=t_st->tm_hour;
      break;
    case 4:
      myResult=t_st->tm_min;
      break;
    case 5:
      myResult=t_st->tm_sec;
      break;
    case 6:
      myResult=t_st->tm_wday;
      break;
  }
  return myResult;
}

void setup()
{
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);
  u8g2.begin();
  u8g2.setFont(u8g2_font_10x20_me);
  u8g2.disableUTF8Print();
  WiFi.disconnect();
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(_lwifi_ssid, _lwifi_pass);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  delay(300);
  digitalWrite(LED_BUILTIN, HIGH);
  configTime(8*3600, 0, "time.stdtime.gov.tw","time.nist.gov");
  while(get_data_from_RTC(0)<2000){delay(500);}
}

void loop()
{
  Date = String(get_data_from_RTC(0))+String("/")+String(get_data_from_RTC(1))+String("/")+String(get_data_from_RTC(2));
  Time = String(get_data_from_RTC(3))+String(":")+String(get_data_from_RTC(4))+String(":")+String(get_data_from_RTC(5));
  Serial.println(Date);
  Serial.println(Time);
  Display(Date, Time);
  delay(1000);
}
