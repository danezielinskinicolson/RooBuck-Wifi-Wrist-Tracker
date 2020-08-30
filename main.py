# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:03:03 2020

@author: Dane

"""

import Extract_Data as ED
import RSSICalculations as RSSI_C

Scansest = ED.Extract_Scans()
testvalues = [-41,-41,-36,-42,-44,-39,-39,-44,-42,-45]
testvaluesshort = [-34,-38,-38,-39,-38,-39,-41,-39,-38,-40]
sumv = 0
for i in testvalues:
    sumv = sumv + i
A0 = sumv/len(testvalues)
d = RSSI_C.RSSI_to_Distance(testvaluesshort,A_0 = A0)
