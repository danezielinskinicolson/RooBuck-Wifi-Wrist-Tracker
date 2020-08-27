# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:14:33 2020

@author: Dane
"""
import math

def RSSI_to_Distance(RSSI, n = 1, d_0 = 1, A_0 = 1):
    d = []
    for i in RSSI:
        value = d_0*10**((i-A_0)/(-10*n))
        d.append(value) 
    return d
    