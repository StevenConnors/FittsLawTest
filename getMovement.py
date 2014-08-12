# Get the Movement of the mouse using Fitts' Law data.
# Zhen Li, Aug. 8th, 2014.

from pylab import *
import numpy as np
import Tkinter, Tkconstants, tkFileDialog
import os
from bisect import bisect_left
import dataReader as dr

def getTrace(files):
    " Get the trace of cursor "

    traceMat, clickMat = [], []
    for fileObj in files:
        fileExt = os.path.splitext(fileObj.name)[1]
        if fileExt == '.trk':
            try:
                traceMat = np.genfromtxt(fileObj.name, dtype = float, delimiter = ',',\
                    skiprows = 1, names = True, comments = '/')
            except:
                traceMat = np.genfromtxt(fileObj.name, dtype = float, delimiter = ',',\
                    skiprows = 2, names = True, comments = '/')
        elif fileExt == '.dat':
            clickMat = np.genfromtxt(fileObj.name, dtype = float, delimiter = ',',\
                skiprows = 2, names = True, comments = '/')
            print str(clickMat.dtype)

    # print traceMat['Target']
    return traceMat, clickMat

def getVecLen(vec):
    " Get the length of the vector"

    length = np.sqrt(np.sum(np.square(vec)))
    return length

def getOutlier(files):
    " Get the outlier data. This function is part of Julian's 'dataAnalysis.py' "
    outlier = []
    for fileObj in files:
        fileExt = os.path.splitext(fileObj.name)[1]
        if fileExt == '.dat':
            data=dr.csvReader(fileObj.name, ',', 4)
            print data
            header={}
            for i in range(len(data['header'][2])):
                header[data['header'][2][i].strip()]=i
            
            fittsData={'movementTime':[],'error':[],'width':[],'distance':[],'clickX':[],'clickY':[],'wrongClick':[],\
                       'targetX':[],'targetY':[],'dist2Tar':[],'movDistance':[],\
                       'outliers':[]}
            
            
            
            for i in data['data']:
                if fittsData['movementTime']!=[]:
                    tempTime=float(i[1])-lastTime
                    lastTime=float(i[1])
                else:
                    tempTime=float(i[1])
                    lastTime=float(i[1])
                fittsData['movementTime'].append(tempTime)
                fittsData['error'].append(float(i[header['errorMargin']]))
                fittsData['width'].append(float(i[header['width']]))
                fittsData['distance'].append(float(i[header['distance']]))
                fittsData['clickX'].append(float(i[header['clickX']]))
                fittsData['clickY'].append(float(i[header['clickY']]))
                fittsData['wrongClick'].append(float(i[header['clicked']]))
                fittsData['targetX'].append(float(i[header['targetX']]))
                fittsData['targetY'].append(float(i[header['targetY']]))
                
            #Effective width calculation
            for i in range(len(fittsData['movementTime'])):
                if fittsData['wrongClick'][i]!=1:
                    a=[fittsData['targetX'][i],fittsData['targetY'][i]]
                    b=[fittsData['clickX'][i],fittsData['clickY'][i]]
                    a=np.array(a)
                    b=np.array(b)
                    fittsData['dist2Tar'].append(np.linalg.norm(a-b))
                    
                    if i>0:
                        p=[fittsData['clickX'][i-1],fittsData['clickY'][i-1]]
                        p=np.array(p)
                        fittsData['movDistance'].append(np.linalg.norm(a-p))
                        
                    else:
                        fittsData['movDistance'].append(-1)
                else:
                    fittsData['movDistance'].append(-1)
                
            we=4.133*np.std(fittsData['dist2Tar'])
            
    #         de=np.mean(fittsData['movDistance'])
            de=[fittsData['movDistance'][i] for i in range(len(fittsData['movDistance'])) if fittsData['movDistance'][i]!=-1]
            meanDe=np.mean(de)
            stdDistance=np.std(de)
            
            mvt=[fittsData['movementTime'][i] for i in range(len(fittsData['wrongClick'])) if fittsData['wrongClick'][i]==0]
            meanMvt=np.mean(mvt)
            stdMvt=np.std(mvt)
            
            #Outlier Detection
            outlier=[0 for i in range(len(fittsData['movementTime']))]
            for i in range(len(fittsData['movementTime'])):
                if fittsData['movDistance'][i]!=-1:
                    if np.abs(fittsData['movementTime'][i]-meanMvt)>=3*stdMvt or \
                    np.abs(fittsData['movDistance'][i]-meanDe)>=3*stdDistance:
                        outlier[i]=1
                        print(fittsData['movDistance'][i],fittsData['movementTime'][i])
                        print(meanDe,stdDistance,meanMvt,stdMvt)
                    else:
                        outlier[i]=0
                else:
                    outlier[i]=1
    return outlier

def run():
    " Main procedure "

    tkObj = Tkinter.Tk()
    tkObj.file_opt = options = {}
    options['defaultextension'] = '.trk'

    # trkKeys = ['Target', 'times', 'x', 'y']

    fi = 0
    openFiles = tkFileDialog.askopenfiles('r')
    if openFiles:
        # The matrix of movement data and click(target) data
        traceMat, clickMat = getTrace(openFiles)
        
        targetNum, traceX, traceY, times = traceMat['Target'], traceMat['x'], traceMat['y'], traceMat['times']
        targetNum = [int(x) for x in targetNum]
        targetX, targetY = clickMat['targetX'], clickMat['targetY']
        # Note: the ideal distance is not used, because the clicking positions vary.
        distance = clickMat['distance'][0]
        
        # Get the valid data sets
        outlier = getOutlier(openFiles)
        print 'outlier vec: ' + str(outlier)


        startCircle = bisect_left(targetNum, 1)
        # endCircle = bisect_left(targetNum, 4)
        endCircle = len(targetNum)

        # Show the raw movement in 2-D graph
        figure(fi)
        fi += 1
        plot(traceX[startCircle:endCircle], traceY[startCircle:endCircle], 'b')
        plot(traceX[startCircle:endCircle], traceY[startCircle:endCircle], 'g.')
        title('Raw Data')

        # Calculate and show the deviation from straight path
        # Note: calculate from the second circle. Because the path of the mouse 
        # from the start point to the first circle is useless.
        deviationData = []
        devX, devY = [], []
        upVec = np.array([0,1])

        i = startCircle
        while i < endCircle:
        # for i in range(startCircle, endCircle):
            if targetNum[i-1] != targetNum[i]:
                # New target start
                currTarget = targetNum[i]
                currStart = currTarget - 1
                if outlier[currStart] == 1:
                    # Invalid: move to a valid one
                    i = bisect_left(targetNum, currTarget + 1, i)
                    print 'skip data: No.{} to No.{}'.format(str(currStart), str(currTarget))
                    continue

                x0, y0 = traceX[i], traceY[i]
                straightVec = np.array([ targetX[currTarget] - x0, targetY[currTarget] - y0 ])
                straightLen  = getVecLen(straightVec)
                print 'straightLen: ' + str(straightLen)
                devX, devY = [], []

                #print on the raw graph
                straightX = np.linspace(x0, targetX[currTarget], 50)
                straightY = np.linspace(y0, targetY[currTarget], 50)
                plot(straightX, straightY, 'r')

            # Normal point
            currVec = np.array([ traceX[i] - x0, traceY[i] - y0 ])
            
            # Note: the projLen is positive/negative
            projLen = np.sum(currVec * straightVec) / straightLen 
            projVec = projLen / straightLen  * straightVec
            
            perpVec = currVec - projVec
            perpLen = getVecLen(perpVec)
            if sum(perpVec * upVec) < 0:
                perpLen = -perpLen

            # print straightVec, currVec, projVec, perpVec, getVecLen(currVec), projLen, perpLen

            devX.append(projLen)
            devY.append(perpLen)

            if i+1 == endCircle or targetNum[i+1] != targetNum[i]:
                # End of this set
                deviationData.append([devX, devY])
            i += 1
            
        figure(fi)
        fi += 1
        for devPoints in deviationData:
            plot(devPoints[0], devPoints[1], 'b')
            plot(devPoints[0], devPoints[1], 'g.', markersize = 3)
        title('Deviation from Straight Path')
        axis([-80, distance + 80, -80, 80])



    show()

run()
