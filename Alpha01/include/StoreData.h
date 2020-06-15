
#include "Arduino.h"
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
class StoreData {
private:

public:
    // class constructors
    StoreData();
    // variable constructors
    const char* RSSI_1;
    // function constructors
    int32_t getRSSI(const char* RSSI_1);
};
