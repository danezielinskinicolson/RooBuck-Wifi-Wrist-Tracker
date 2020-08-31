import re

import numpy as np
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt


def Extract_Scans(LogAddress = 'ESP_Log_Calibration'):
    mylines = []                             # Declare an empty list named mylines.
    with open (LogAddress, 'rt') as myfile: # Open lorem.txt for reading text data.
        for myline in myfile:                # For each line, stored as myline,
            mylines.append(myline)           # add its contents to mylines.
    GridValues = []
    for i in mylines:
        i = i.replace("\'b\'","")
        
        TimeData = i.split("Data Start: ")[0]
        NetworkData = i.split("Data Start: ")[1]
        NetworkData = NetworkData.split("   End")[0]
        
        GridposData = NetworkData.split("Scan N0: ")[0]
        GridposData = GridposData.split("X")[1:3]
        
        ScanData = NetworkData.split("Scan N0: ")[1:]
        KeyData = [[],[],[],[]]
        for j in ScanData:
            #remove the N0 value
            j = re.split("Scan Start:X|ScanStart:X",j)[-1]
#            
            print(j)
            
            SSIDData = []
            RSSIData = []
            
            
            counter = 0
            j = j.split("X")
            for k in j:
                if counter == 0:
                    SSIDData.append(k)
                elif counter == 1:
                    RSSIData.append(k)
                    counter = -1
                counter = counter + 1
            counter = 0
            
            for l in SSIDData:
                if l == "test_A":
                    KeyData[0].append(int(RSSIData[counter]))
                if l == "Test_b":
                    KeyData[1].append(int(RSSIData[counter]))
                if l == "Test_c":
                    KeyData[2].append(int(RSSIData[counter]))
                if l == "Test_d":
                    KeyData[3].append(int(RSSIData[counter]))
                    
                counter = counter + 1
        KeyData.append(GridposData)
        GridValues.append(KeyData)
    return GridValues

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def GridData(Extracted_scans):
    bigGrid = [ [0] * 6 for _ in range(5)]
    for i in Extracted_scans:
        #print([int(i[4][0])],[int(i[4][1])])
        if int(i[4][1]) <= 5 :
            vals = [0,1,2,3]
            for counter in vals:
                i[counter] = np.array(i[counter])
                i[counter] = reject_outliers(i[counter], m=2)
                i[counter] = np.average(i[counter])
                
            bigGrid[int(i[4][0])][int(i[4][1])] = i
    return bigGrid

def InterpolatedGrid(CornerGrid,SquareGrid,dist,Router):
    row_Counter = 0
    for row in SquareGrid:
        col_Counter = 0
        for col in row:
            #get the 4 relevant corners
            col_corners = [CornerGrid[row_Counter][col_Counter][4][1],CornerGrid[row_Counter][col_Counter + 1][4][1]]
            row_corners = [CornerGrid[row_Counter][col_Counter][4][0],CornerGrid[row_Counter + 1][col_Counter][4][0]]
            
            
            corners = [[col_corners[0],row_corners[0]],[col_corners[1],row_corners[0]],[col_corners[0],row_corners[1]],[col_corners[1],row_corners[1]]]
            print(Router)
            a_zcorners = [CornerGrid[row_Counter][col_Counter][Router],CornerGrid[row_Counter][col_Counter + 1][Router],\
                          CornerGrid[row_Counter + 1][col_Counter][Router],CornerGrid[row_Counter + 1][col_Counter +1][Router]]
            print(a_zcorners)
            SquareGrid[row_Counter][col_Counter] = InterpolateGridRSSI(corners,a_zcorners,dist)
            col_Counter = col_Counter + 1
        row_Counter = row_Counter + 1
    return SquareGrid

def InterpolateGridRSSI(corners,zcorners,dist):
    x,y = np.mgrid[int(corners[0][0])*dist:int(corners[1][0])*dist:0.05, int(corners[0][1])*dist:int(corners[2][1])*dist:0.05]
    
    xcorners = x[0,0], x[0, -1], x[-1, 0], x[-1, -1]
    ycorners = y[0,0], y[0, -1], y[-1, 0], y[-1, -1]
    #zcorners = [4, 2, 3, 4]
    
    xy = np.column_stack([xcorners, ycorners])
    xyi = np.column_stack([x.ravel(), y.ravel()])
    zi = scipy.interpolate.griddata(xy, zcorners, xyi)
    zi = zi.reshape(x.shape)
    
    
#    fig, ax = plt.subplots()
#    grid = ax.pcolormesh(x, y, zi)
#    ax.scatter(xcorners, ycorners, c=zcorners, s=200)
#    fig.colorbar(grid)
#    ax.margins(0.05)

    return [x,y,zi]

def Plot_RSSI_Map(SquareGridz):
    X = []
    Y = []
    Zi = []
    for row in SquareGridz:
        #stich cols together
        currentx = []
        currenty = []
        currentz = []
        for col in row:
            if currentx == []:
                currentx = col[0]
            else:
                currentx = np.vstack((currentx, col[0]))
                
            if currenty == []:
                currenty = col[1]
            else:
                currenty = np.vstack((currenty, col[1]))   
                
            if currentz == []:
                currentz = col[2]
            else:
                currentz = np.hstack((currentz, col[2]))             
                
        Previousx = currentx.T
        Previousy = currenty.T
        Previousz = currentz
        
        if X == []:
            X = Previousx
        else:
            X = np.vstack((Previousx,X))
            
        if Y == []:
            Y = Previousy
        else:
            Y = np.vstack((Y,Previousy))
            
        if Zi == []:
            Zi = Previousz
        else:
            Zi = np.vstack((Zi,Previousz))
        #stich rows together
    #
    #corners = [[0,0.5],[0.5,1]]
    zcorners = [Zi[0][0],Zi[0][1],Zi[1][0],Zi[1][1]]
    
    
    #[x,y,zi] = InterpolateGridRSSI(corners,zcorners)
    xcorners = X[0,0], X[0, -1], X[-1, 0], X[-1, -1]
    ycorners = Y[0,0], Y[0, -1], Y[-1, 0], Y[-1, -1]
    #zcorners = [4, 2, 3, 4]
    
    #####Plotting grid
    plt.figure(figsize=(10, 15))
    fig, ax = plt.subplots()
    grid = ax.pcolormesh(X, Y, Zi)
    #ax.scatter(xcorners, ycorners, c=zcorners, s=200)
    fig.colorbar(grid)
    ax.margins(0.05)
    
    plt.show()

e = Extract_Scans(LogAddress = 'ESP_Log_Calibration.txt')

CornerGrid = GridData(e)
SquareGrida = [ [0] * 5 for _ in range(4)]
SquareGridb = [ [0] * 5 for _ in range(4)]
SquareGridc = [ [0] * 5 for _ in range(4)]
SquareGridd = [ [0] * 5 for _ in range(4)]

SquareGrida = InterpolatedGrid(CornerGrid,SquareGrida,0.5,0)
SquareGridb = InterpolatedGrid(CornerGrid,SquareGridb,0.5,1)
SquareGridc = InterpolatedGrid(CornerGrid,SquareGridc,0.5,2)
SquareGridd = InterpolatedGrid(CornerGrid,SquareGridd,0.5,3)

Plot_RSSI_Map(SquareGrida)
Plot_RSSI_Map(SquareGridb)
Plot_RSSI_Map(SquareGridc)
Plot_RSSI_Map(SquareGridd)


