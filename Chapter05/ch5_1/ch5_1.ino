//Generated Date: Wed, 31 Jul 2024 06:15:54 GMT

#include <WiFi.h>

char _lwifi_ssid[] = "JackJean";
char _lwifi_pass[] = "0226852016";

void setup()
{
  Serial.begin(115200);

  WiFi.disconnect();
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(_lwifi_ssid, _lwifi_pass);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  delay(300);
  Serial.println("WiFi連線成功!");
  Serial.println((String("IP是 ")+String(WiFi.localIP().toString())));
}

void loop()
{

}
