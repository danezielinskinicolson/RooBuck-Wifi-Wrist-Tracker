# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:03:03 2020

@author: Dane
"""
import Extract_Data as ED
import RSSICalculations as RSSI_C

Scansest = ED.Extract_Scans()

d = RSSI_C.RSSI_to_Distance([-53,-54,-54,-53])