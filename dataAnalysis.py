import numpy as np
import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
import dataReader as dr

tkObj=Tkinter.Tk()
tkObj.file_opt = options = {}
options['defaultextension'] = '.txt'
X=[]
Y=[]
  
a=tkFileDialog.askopenfile('r')
if a:
    data=dr.csvReader(a.name, ',', 4)
    
    fittsData={'movementTime':[],'error':[],'width':[],'distance':[],'clickX':[],'clickY':[],'wrongClick':[]}
    
    
    
    for i in data['data']:
        if fittsData['movementTime']!=[]:
            tempTime=float(i[1])-lastTime
            lastTime=float(i[1])
        else:
            tempTime=float(i[1])
            lastTime=float(i[1])
        fittsData['movementTime'].append(tempTime)
        fittsData['error'].append(float(i[-1]))
        fittsData['width'].append(float(i[8]))
        fittsData['distance'].append(float(i[9]))
        fittsData['clickX'].append(float(i[4]))
        fittsData['clickY'].append(float(i[5]))
        fittsData['wrongClick'].append(float(i[6]))
        
        
    #Fitts law coefficients
    for i in range(len(fittsData['movementTime'])):
        if fittsData['wrongClick']!=1:
            
            Y.append(fittsData['movementTime'][i])
            dist=fittsData['distance'][i]
            width=fittsData['width'][i]
    #         eWidth=width*
            
            #1 is added to calculate the intercept
            X.append([1,np.log2(dist/width+1)])
        
    Y=np.array(Y)
    X=np.array(X)
    Xt=np.transpose(X)
    c=np.dot(np.dot(np.linalg.inv(np.dot(Xt,X)),Xt),Y)
    print(c)
    IP=1/c[1]
    print(IP)
    
    
    