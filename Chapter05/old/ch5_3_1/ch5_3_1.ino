//Generated Date: Mon, 05 Aug 2024 07:06:06 GMT

String Token = "你的LINE權杖";
#include <WiFi.h>
#include <WiFiClientSecure.h>

char _lwifi_ssid[] = "你的WiF熱點帳號";
char _lwifi_pass[] = "你的WiF熱點帳號";

String LineNotify(String token, String request) {
  String getAll="", getBody="";
  request.replace("%","%25");
  request.replace(" ","%20");
  //request.replace("&","%26");
  request.replace("#","%23");
  request.replace("\"","%22");
  request.replace("\n","%0D%0A");
  request.replace("%20stickerPackageId","&stickerPackageId");
  request.replace("%20stickerId","&stickerId");
  request.replace("%20imageFullsize","&imageFullsize");
  request.replace("%20imageThumbnail","&imageThumbnail");
  WiFiClientSecure client_tcp;
  client_tcp.setInsecure();
  if (client_tcp.connect("notify-api.line.me", 443)) {
    client_tcp.println("POST /api/notify HTTP/1.1");
    client_tcp.println("Connection: close");
    client_tcp.println("Host: notify-api.line.me");
    client_tcp.println("User-Agent: ESp8266/1.0");
    client_tcp.println("Authorization: Bearer " + token);
    client_tcp.println("Content-Type: application/x-www-form-urlencoded");
    client_tcp.println("Content-Length: " + String(request.length()));
    client_tcp.println();
    client_tcp.println(request);
    client_tcp.println();
    boolean state = false;
    long startTime = millis();
    while ((startTime + 3000) > millis()) {
      while (client_tcp.available()) {
        char c = client_tcp.read();
        if (c == '\n') {
          if (getAll.length()==0) state=true;
           getAll = "";
        }
        else if (c != '\r')
          getAll += String(c);
          if (state==true) getBody += String(c);
          startTime = millis();
        }
        if (getBody.length()!= 0) break;
      }
      client_tcp.stop();
      Serial.println(getBody);
  }
  else {
    getBody="Connected tonotify-api.line.me failed.";
    Serial.println("Connected to notify-api.line.me failed.");
  }
  return getBody;
}

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  WiFi.disconnect();
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(_lwifi_ssid, _lwifi_pass);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  delay(300);
  digitalWrite(LED_BUILTIN, HIGH);
  LineNotify(Token, "message="+String((String("您好!")+String("\n")+String("這是測試訊息"))));
  LineNotify(Token, "message="+String("嗨!")+"&stickerPackageId="+String(1)+"&stickerId="+String(2));
}

void loop()
{

}
