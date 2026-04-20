//Generated Date: Tue, 06 Aug 2024 08:37:35 GMT

int VR = 0;
#include <WiFi.h>
#include <WiFiClientSecure.h>

char _lwifi_ssid[] = "你的WiF熱點帳號";
char _lwifi_pass[] = "你的WiF熱點密碼";

String Spreadsheet_insert(String func, String data, int row, int col, String text, String mySpreadsheeturl, String mySpreadsheetname, String myScript) {
  data = urlencode(data);
  text = urlencode(text);
  mySpreadsheeturl = urlencode(mySpreadsheeturl);
  mySpreadsheetname = urlencode(mySpreadsheetname);
  const char* myDomain = "script.google.com";
  String getAll="", getBody = "";
  Serial.println("Connect to " + String(myDomain));
  WiFiClientSecure client_tcp;
  client_tcp.setInsecure();
  if (client_tcp.connect(myDomain, 443)) {
    Serial.println("Connection successful");
    String Data = "&func="+func+"&data="+data+"&spreadsheeturl="+mySpreadsheeturl+"&spreadsheetname="+mySpreadsheetname;
    Data += "&row="+String(row)+"&col="+String(col)+"&text="+text;
    client_tcp.println("POST " + myScript + " HTTP/1.1");
    client_tcp.println("Host: " + String(myDomain));
    client_tcp.println("Content-Length: " + String(Data.length()));
    client_tcp.println("Content-Type: application/x-www-form-urlencoded");
    client_tcp.println("Connection: close");
    client_tcp.println();
    int Index;
    for (Index = 0; Index < Data.length(); Index = Index+1024) {
      client_tcp.print(Data.substring(Index, Index+1024));
    }
    int waitTime = 10000;
    long startTime = millis();
    boolean state = false;

    while ((startTime + waitTime) > millis())
    {
      Serial.print(".");
      delay(100);
      while (client_tcp.available())
      {
          char c = client_tcp.read();
          if (state==true) getBody += String(c);
          if (c == '\n')
          {
            if (getAll.length()==0) state=true;
            getAll = "";
          }
          else if (c != '\r')
            getAll += String(c);
          startTime = millis();
       }
       if (getBody.length()>0) break;
    }
    client_tcp.stop();
  }
  else {
    Serial.println("Connected to " + String(myDomain) + " failed.");
  }

  return getBody;
}

String urlencode(String str) {
  const char *msg = str.c_str();
  const char *hex = "0123456789ABCDEF";
  String encodedMsg = "";
  while (*msg != '\0') {
    if (('a' <= *msg && *msg <= 'z') || ('A' <= *msg && *msg <= 'Z') || ('0' <= *msg && *msg <= '9') || *msg == '-' || *msg == '_' || *msg == '.' || *msg == '~') {
      encodedMsg += *msg;
    } else {
      encodedMsg += '%';
      encodedMsg += hex[(unsigned char)*msg >> 4];
      encodedMsg += hex[*msg & 0xf];
    }
    msg++;
  }
  return encodedMsg;
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
  pinMode(34, INPUT);
}

void loop()
{
  VR = analogRead(34);
  Serial.println(VR);
  Spreadsheet_insert("insertlast", String("gmt_datetime")+"|"+String(VR), 0, 0, "", String("你的Google試算表網址"), String("工作表1"), "/macros/s/AKfycbxA3hhTlntwVTOcqngOC_iJL_zLmRwzcDbMYDs7FD8iinNsY9XZsMkD7AcXTIUbEc33EA/exec");
  delay(20000);
}
