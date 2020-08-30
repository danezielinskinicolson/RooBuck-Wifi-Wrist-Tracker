# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 12:48:18 2020

@author: Dane
"""
import re

def Extract_Scans(LogAddress = 'ESP_Logs\ESP_Log_.txt'):
    mylines = []                             # Declare an empty list named mylines.
    with open (LogAddress, 'rt') as myfile: # Open lorem.txt for reading text data.
        for myline in myfile:                # For each line, stored as mylin/e,
            mylines.append(myline)           # add its contents to mylines.
    
    
    
    dataPerScan = []
    for i in mylines:
    #    i = i.replace("\'b\'   ","   ")
    #    i = i.replace("   \'b\'","   ")
        i = i.replace("\'b\'","")
        TimeData = i.split("Data Start:X")[0]
        Imu = i.split("Data Start:X")[1].split("Scan Start:")[0]
        NetworkData = i.split("Scan Start:X")[1]
        NetworkData = NetworkData.split("   End")[0]
    
        
        ImuSplit = re.split("\'b\'|X|\'b\'X|X\'b\'",Imu)
        counter = 0
        Ax = []
        Ay = []
        Az = []
        IMUTimeSignature = []
        for j in ImuSplit:
            if counter == 0:
                Ax.append(int(j))
            elif counter == 1:
                Ay.append(int(j))
            elif counter == 2:
                Az.append(int(j))
            elif counter == 3:
                IMUTimeSignature.append(int(j))
                counter = -1
            counter = counter + 1
        
        SSIDData = []
        RSSIData = []
        
        counter = 0
        NetworkData = re.split("\'b\'|X|\'b\'X|X\'b\'",NetworkData)
        for k in NetworkData:
            if counter == 0:
                SSIDData.append(k)
            elif counter == 1:
                RSSIData.append(int(k))
                counter = -1
            counter = counter + 1
        
        TimeData = TimeData.split(" AUS Eastern Standard Time   b\'")[0]
        TimeData = TimeData.split(" ")
        dataPerScan.append([Ax,Ay,Az,IMUTimeSignature,SSIDData,RSSIData,TimeData])
    return dataPerScan
    #print(mylines)
