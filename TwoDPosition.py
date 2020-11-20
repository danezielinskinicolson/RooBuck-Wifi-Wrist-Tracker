# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:03:03 2020

@author: Dane

"""
import numpy as np

import Extract_Data as ED
import RSSICalculations as RSSI_C


def trilaterate2D(NetworkLocations, NetworkDistances):
    x1 = NetworkLocations[0][0]
    x2 = NetworkLocations[1][0]
    x3 = NetworkLocations[2][0]
    y1 = NetworkLocations[0][1]
    y2 = NetworkLocations[1][1]
    y3 = NetworkLocations[2][1]
    Points = []
    for i in range(0,min([len(NetworkDistances[0]),len(NetworkDistances[1]),len(NetworkDistances[2])])):
        r1 = NetworkDistances[0][i]
        r2 = NetworkDistances[1][i]
        r3 = NetworkDistances[2][i]
        points = circleIntersection(x1,x2,x3,y1,y2,y3,r1,r2,r3)
        Points.append(points)
    return Points

def circleIntersection(x1,x2,x3,y1,y2,y3,r1,r2,r3):
    x = ((y2-y3)*((y2**2-y1**2)+(x2**2-x1**2)+(r1**2-r2**2))-(y1-y2)*((y3**2-y2**2)+(x3**2-x2**2)+(r2**2-r3**2)))/(2*((x1-x2)*(y2-y3)-(x2-x3)*(y1-y2)))
    y = ((x2-x3)*((x2**2-x1**2)+(y2**2-y1**2)+(r1**2-r2**2))-(x1-x2)*((x3**2-x2**2)+(y3**2-y2**2)+(r2**2-r3**2)))/(2*((y1-y2)*(x2-x3)-(y2-y3)*(x1-x2)))
    return [x,y]

def GetPosition(inputFile = 'ESP_Logs\ESP_Log_Prtot3Test.txt'):
    NetworkIDs = ["uniwide","UNSW Guest","eduroam","Global_Students"]
    NetworkLocations = [[0,0],[0,2.5],[4.5,0],[4.5,2.5]]
    NetworkRSSIs = [[],[],[],[]]
    NetworkDistances = [[],[],[],[]]
    Points = []
    PosTimes= []
    Scansest = ED.Extract_Scans(inputFile)
    
    counter = 0
    for k in NetworkIDs:
        for i in Scansest:
            PosTimes.append(i[6][0])
            for j in range(0,len(i[4])):
                if i[4][j] == k:
                    NetworkRSSIs[counter].append(i[5][j])
        counter = counter + 1
     
    testvalues = [-41,-41,-36,-42,-44,-39,-39,-44,-42,-45]
    testvaluesshort = [-34,-38,-38,-39,-38,-39,-41,-39,-38,-40]
    sumv = 0
    
    for i in testvalues:
        sumv = sumv + i
    A0 = sumv/len(testvalues)               
            
    counter = 0
    for k in NetworkRSSIs:
        d = RSSI_C.RSSI_to_Distance(k,A_0 = A0)
        NetworkDistances[counter] = d
        counter = counter + 1
    print(len(NetworkDistances[0]))
    Points = trilaterate2D(NetworkLocations, NetworkDistances)
    return [Points,PosTimes]
Points = GetPosition()