
#include "Arduino.h"
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
class StoreData {
private:

public:
    // class constructors
    StoreData();
    // variable constructors
    String SSID_1;
    String SSID_2;
    String SSID_3;
    String SSID_4;

    char FinalMessage[1024];

    int32_t RSSI_1;
    int32_t RSSI_2;
    int32_t RSSI_3;
    int32_t RSSI_4;
    

    // function constructors
    int32_t getRSSI(String SSID_1);
    String ComposeMessage(String SSID_1, String SSID_2, String SSID_3, String SSID_4, int32_t RSSI_1, int32_t RSSI_2, int32_t RSSI_3, int32_t RSSI_4 );
};
