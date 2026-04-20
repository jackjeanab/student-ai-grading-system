//Generated Date: Tue, 18 Jun 2024 07:09:29 GMT

#include <LWiFi.h>

char _lwifi_ssid[] = "你的WiFi熱點帳號";
char _lwifi_pass[] = "你的WiF熱點密碼";

void setup()
{
  Serial.begin(115200);

  while (WiFi.begin(_lwifi_ssid, _lwifi_pass) != WL_CONNECTED) { delay(1000); }
  Serial.println("WiFi連線成功!");
  Serial.println((String("IP是 ")+String(WiFi.localIP().toString())));
}

void loop()
{

}
