//Generated Date: Thu, 08 Aug 2024 07:42:58 GMT

String ReData = "";
#include <WiFi.h>
#include <PubSubClient.h>
#define MQTT_USER ""
#define MQTT_PASSWORD ""

char _lwifi_ssid[] = "你的WiF熱點帳號";
char _lwifi_pass[] = "你的WiFi熱點密碼";
const char* mqtt_server = "broker.mqttgo.io";
const unsigned int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient mqtt_client(espClient);
String mqtt_data = "";

void mqtt_sendText(String topic, String text) {
    String clientId = "";
    if (mqtt_client.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      mqtt_client.publish(topic.c_str(), text.c_str());
    }
}

void reconnect() {
  while (!mqtt_client.connected()) {
    String mqtt_clientId = "";
    if (mqtt_client.connect(mqtt_clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
      mqtt_client.subscribe("Jack/LED");
    } else {
      delay(5000);
    }
  }
}

void setup()
{
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);
  randomSeed(micros());
  mqtt_client.setServer(mqtt_server,mqtt_port);
  mqtt_client.setCallback(callback);
  //mqtt_client.setBufferSize(1024);

  WiFi.disconnect();
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(_lwifi_ssid, _lwifi_pass);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }
  delay(300);
  digitalWrite(LED_BUILTIN, HIGH);
  pinMode(16, OUTPUT);
}

void loop()
{
  if (!mqtt_client.connected()) {
    reconnect();
  }
  mqtt_client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  mqtt_data = "";
  for (int ci = 0; ci < length; ci++) {
    char c = payload[ci];
    mqtt_data+=c;
  }
  if (String(topic)=="Jack/LED"&&mqtt_data!="[]") {
    ReData = mqtt_data;
    Serial.println(ReData);
    if (ReData == "1") {
      digitalWrite(16, 1);
    } else if (ReData == "0") {
      digitalWrite(16, 0);
    }
  }
}
