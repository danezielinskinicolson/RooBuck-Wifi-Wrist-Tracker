#include "StoreData.h"

StoreData::StoreData(){
}


int32_t StoreData::getRSSI(String SSID_1){
    //Serial.println("looking for");
    //Serial.println(SSID_1);
    int32_t Return_RSSI = 2000; //setting to meaningless value
    // WiFi.scanNetworks will return the number of networks found
    int n = WiFi.scanNetworks();
    //Serial.println("scan done");
    if (n == 0){
        //Serial.println("no networks found");
    }

    else
    {
        for (int i = 0; i < n; ++i)
        {
            delay(10);
            if (WiFi.SSID(i) == SSID_1){
                //if the network is on list: get the RSSI
                //Serial.println("FOUND ");
                //Serial.println(WiFi.RSSI(i));
                Return_RSSI = WiFi.RSSI(i);
            }
        }
    }
    return Return_RSSI;
}

String StoreData::ComposeMessage(String SSID_1, String SSID_2, String SSID_3, String SSID_4, int32_t RSSI_1, int32_t RSSI_2, int32_t RSSI_3, int32_t RSSI_4 ){
    int32_t arrayRSSI[] = {RSSI_1,RSSI_2,RSSI_3,RSSI_4};
    String arraySSID[] = {SSID_1,SSID_2,SSID_3,SSID_4};
    String TotalMessage = "ESP: "; 
    for (int i = 0; i <= 3; i++)
    {
        if (arrayRSSI[i] != 2000) {
            TotalMessage.concat(arraySSID[i]);
            TotalMessage.concat(arrayRSSI[i]);
        }
    }
    Serial.println("G");
    while(!Serial.available());
    String IMUData = Serial.readString();
    TotalMessage.concat(IMUData);
    return TotalMessage;
}