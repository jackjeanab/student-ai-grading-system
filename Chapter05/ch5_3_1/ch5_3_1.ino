//Generated Date: Tue, 12 Aug 2025 02:38:59 GMT

String UserID = "你的LINE user ID";
String Token = "你的LINE權杖";
#include <WiFi.h>
#include <WiFiClientSecure.h>
WiFiClientSecure client;
#include <WiFiClientSecure.h>

char _lwifi_ssid[] = "你的WiF熱點帳號";
char _lwifi_pass[] = "你的WiF熱點i密碼";
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
    initWiFi();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  ljjLineToken =Token;
  ljjLineId = UserID;
  sendLineBotMsg((String("您好！")+String("\\n")+String("這是測試訊息")),0,0);
  sendLineBotMsg("嗨！",1,2);
}

void loop()
{

}
