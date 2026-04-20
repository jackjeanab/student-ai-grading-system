//Generated Date: Tue, 18 Jun 2024 07:33:49 GMT

#include <WiFi.h>
#include <time.h>

char _lwifi_ssid[] = "JackJean";
char _lwifi_pass[] = "0226852016";
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
  Serial.print((String(get_data_from_RTC(0))+String("/")+String(get_data_from_RTC(1))+String("/")+String(get_data_from_RTC(2))+String(" ")));
  Serial.println((String(get_data_from_RTC(3))+String(":")+String(get_data_from_RTC(4))+String(":")+String(get_data_from_RTC(5))));
  delay(1000);
}
