#include "StoreData.h"

StoreData::StoreData(){
}

const char* RSSI_1 = "The_Lair_of_Task_&_Jakiro";

int32_t StoreData::getRSSI(const char* RSSI_1){
    Serial.println("looking for");
    Serial.println(RSSI_1);
    int32_t Return_RSSI = 2000; //setting to meaningless value
    // WiFi.scanNetworks will return the number of networks found
    int n = WiFi.scanNetworks();
    Serial.println("scan done");
    if (n == 0)
        Serial.println("no networks found");
    else
    {
        for (int i = 0; i < n; ++i)
        {
            delay(10);
            if (WiFi.SSID(i) == RSSI_1){
                //if the network is on list: get the RSSI
                Serial.println("FOUND ");
                Serial.println(WiFi.RSSI(i));
                Return_RSSI = WiFi.RSSI(i);
            }
        }
    }
    return Return_RSSI;
}

