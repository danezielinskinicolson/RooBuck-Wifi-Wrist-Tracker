#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <WiFiManager.h>
#include "StoreData.h"
#ifndef STASSID
#define STASSID "INSERT HERE"
#define STAPSK  "INSERT HERE"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.0.9";
const uint16_t port = 8007;

ESP8266WiFiMulti WiFiMulti;
StoreData ModuleData;


void setup() {
  Serial.begin(115200);
  ModuleData.RSSI_1 = "The_Lair_of_Task_&_Jakiro";
  delay(3000);
  // We start by connecting to a WiFi network

  // comment this out if connecting to network for the first time
  WiFiManager wifiManager;
  wifiManager.autoConnect("AutoConnectAP");
  /*
  //THIS IS UNCOMMENTED IF NETWORK NOT STORED IN NON VOL MEMORY
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");
  delay(500);
  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  */
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);
}


void loop() {
  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);
  
  int32_t RSSI_to_Send = ModuleData.getRSSI(ModuleData.RSSI_1);
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    Serial.println("wait a bit");
    delay(50);
    return;
  }

  // This will send the request to the server
  client.println("RSSI_DATA:   " + String(ModuleData.RSSI_1) + "   " + RSSI_to_Send);
  /*
  //read back one line from server
  Serial.println("receiving from remote server");
  String line = client.readStringUntil('\r');
  Serial.println(line);
  */
  Serial.println("closing connection");
  client.stop();

  Serial.println("wait 0.05 sec...");
  delay(50);
}