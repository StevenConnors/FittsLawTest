# Get the Movement of the mouse using Fitts' Law data.
# Zhen Li, Aug. 8th, 2014.

from pylab import *
import numpy as np
import Tkinter, Tkconstants, tkFileDialog
import os
from bisect import bisect_left

def getTrace(files):
    " Get the trace of cursor "

    traceMat, clickMat = [], []
    for fileObj in files:
        fileExt = os.path.splitext(fileObj.name)[1]
        if fileExt == '.trk':
            traceMat = np.genfromtxt(fileObj.name, dtype = float, delimiter = ',',\
                skiprows = 2, names = True, comments = '/')
        elif fileExt == '.dat':
            clickMat = np.genfromtxt(fileObj.name, dtype = float, delimiter = ',',\
                skiprows = 2, names = True, comments = '/')

    # print traceMat['Target']
    return traceMat, clickMat

def getVecLen(vec):
    " Get the length of the vector"

    length = np.sqrt(np.sum(np.square(vec)))
    return length

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
        targetX, targetY, clickX, clickY = clickMat['targetX'], clickMat['targetY'], clickMat['clickX'], clickMat['clickY']
        # Note: the ideal distance is not used, because the clicking positions vary.
        distance = clickMat['distance'][0]
        
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
        for i in range(startCircle, endCircle):
            if targetNum[i-1] != targetNum[i]:
                # New target
                currTarget = targetNum[i]
                currStart = currTarget - 1
                x0, y0 = clickX[currStart], clickY[currStart]
                straightVec = np.array([ targetX[currTarget] - x0, targetY[currTarget] - y0 ])
                straightLen  = getVecLen(straightVec)
                print 'straightLen: ' + str(straightLen)
                devX, devY = [0.], [0.]

                #print on the raw graph
                straightX = np.linspace(x0, targetX[currTarget], 50)
                straightY = np.linspace(y0, targetY[currTarget], 50)
                plot(straightX, straightY, 'r')

            if traceX[i-1] != traceX[i] or traceY[i-1] != traceY[i]:
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
            else:
                print 'skip point No. ' + str(i) 

            if i+1 == endCircle or targetNum[i+1] != targetNum[i]:
                # End of this set
                currVec = np.array([ clickX[currTarget] - x0, clickY[currTarget] - y0 ])
                
                # Note: the projLen is positive/negative
                projLen = np.sum(currVec * straightVec) / straightLen 
                projVec = projLen / straightLen  * straightVec
                
                perpVec = currVec - projVec
                perpLen = getVecLen(perpVec)
                if sum(perpVec * upVec) < 0:
                    perpLen = -perpLen

                devX.append(projLen)
                devY.append(perpLen)

                deviationData.append([devX, devY])
            
        figure(fi)
        fi += 1
        for devPoints in deviationData:
            plot(devPoints[0], devPoints[1], 'b')
            plot(devPoints[0], devPoints[1], 'g.')
        title('Deviation from Straight Path')
        axis([-50, distance + 50, -50, 50])



    show()

run()
