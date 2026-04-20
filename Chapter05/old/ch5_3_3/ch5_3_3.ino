//Generated Date: Fri, 08 Aug 2025 14:44:32 GMT

#include <WiFi.h>
#include <WiFiClientSecure.h>
WiFiClientSecure client;
#include <WiFiClientSecure.h>

char _lwifi_ssid[] = "JackJean";
char _lwifi_pass[] = "0226852016";
void initWiFi() {
  for (int i=0;i<2;i++) {
    WiFi.begin(_lwifi_ssid, _lwifi_pass);

    delay(1000);
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.println(_lwifi_ssid);

    long int StartTime=millis();
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        if ((StartTime+5000) < millis()) break;
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("");
      Serial.print("STAIP address: ");
      Serial.println(WiFi.localIP());
      Serial.println("");

      break;
    }
  }
}

String ljjLineToken ="";
String ljjLineId = "";
void sendLineBotMsg(String myMsg,byte stkPkgId,byte stkId) {
  static WiFiClientSecure line_client;
  line_client.setInsecure();
  myMsg="{\"to\":\""+ljjLineId+"\",\"messages\":[{\"type\":\"text\",\"text\":\""+myMsg+"\"}";
  if (stkPkgId>0 && stkId>0)
    myMsg+=",{\"type\":\"sticker\",\"packageId\":\""+String(stkPkgId)+"\",\"stickerId\":\""+String(stkId)+"\"}";
  myMsg+="]}";
  Serial.println(myMsg);
  if (line_client.connect("api.line.me", 443)) {
    line_client.println("POST /v2/bot/message/push HTTP/1.1");
    line_client.println("Connection: close");
    line_client.println("Host: api.line.me");
    line_client.println("Authorization: Bearer " + ljjLineToken);
    line_client.println("Content-Type: application/json; charset=utf-8");
    line_client.println("Content-Length: " + String(myMsg.length()));
    line_client.println();
    line_client.println(myMsg);
    line_client.println();
    line_client.stop();
  }
  else {
    Serial.println("Line Bot push failed");
  }
}

void setup()
{
  Serial.begin(115200);

    initWiFi();
  ljjLineToken ="tdyEbxfwzvQ1zPkjtYdXPVGsPIsi2iA2/eD8pJR19UQuCzuKEPmr2sQOtagFgxD+DbKEXQ18g7bQY5L5IYsc9/ABTMEbBNrqzQpDMNqfdfmyHEbZOvjXG6iYA/A2efNOxDOIpWe2rZrMLPPxrjPv7AdB04t89/1O/w1cDnyilFU=";
  ljjLineId = "U46925a783f3611c2dd6d1eb086767a1a";
  sendLineBotMsg((String("JackJean")+String("\\n")+String("測試")),1,1);
}

void loop()
{

}
