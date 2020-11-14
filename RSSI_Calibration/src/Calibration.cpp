#include <Arduino.h>
#include "WiFi.h"


//Wifi info 

const char* ssid = "Network";
const char* password = "Password";

const uint16_t port = 8007;
const char * host = "192.168.0.9";
String data;

String xpos;
String ypos;
String testN0;

String tab = "X";

void SendData(String data){
  WiFiClient client;
 
  if (!client.connect(host, port)) {
 
    Serial.println("Connection to host failed");
 
    delay(1000);
    return;
  }
  client.print(data);
  client.stop();
}

String WifiScan_Update(){
  Serial.println("scan start");
  String ScanString = "Scan Start:";
  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0) {
    Serial.println("no networks found");
  } else {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
      ScanString = ScanString + tab + WiFi.SSID(i) + tab + WiFi.RSSI(i);
    }
  }
  Serial.println("");
  return ScanString;
}

void setup() {
  Serial.begin(115200);

    // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
    
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("Setup done");

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("Enter your Test number");
  while(Serial.available() == 0){}
  testN0 = Serial.read() -48;
  Serial.print("Enter your x position");
  while(Serial.available() == 0){}
  xpos = Serial.read()-48;
  Serial.print("Enter your y position");
  while(Serial.available() == 0){}
  ypos = Serial.read()-48;


  data = "Data Start: ";
  String ScanIter = "Scan N0: ";
  data = data + testN0 + tab + xpos + tab + ypos + tab;
  int counter = 0;
  while(counter < 10){
    data = data + tab + ScanIter + counter + tab + WifiScan_Update();
    counter ++;
    delay(40);
  }
  data = data + "   End";
  SendData(data);
  delay(1000);
}