
import numpy as np
import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
import dataReader as dr

tkObj=Tkinter.Tk()
tkObj.file_opt = options = {}
options['defaultextension'] = '.dat'
X=[]
Y=[]
  
a=tkFileDialog.askopenfiles('r')
if a:
    for file in a:
        data=dr.csvReader(file.name, ',', 4)
        header={}
        for i in range(len(data['header'][2])):
            header[data['header'][2][i].strip()]=i
        
        fittsData={'movementTime':[],'error':[],'width':[],'distance':[],'clickX':[],'clickY':[],'wrongClick':[],\
                   'targetX':[],'targetY':[],'dist2Tar':[],'movDistance':[]}
        
        
        
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
                    if fittsData['wrongClick'][i-1]!=1:
                        p=[fittsData['clickX'][i-1],fittsData['clickY'][i-1]]
                        p=np.array(p)
                        fittsData['movDistance'].append(np.linalg.norm(a-p))
            
            
        we=4.133*np.std(fittsData['dist2Tar'])
        de=np.mean(fittsData['movDistance'])
            
        #Fitts law coefficients
        for i in range(len(fittsData['movementTime'])):
            if fittsData['wrongClick']!=1:
                
                Y.append(fittsData['movementTime'][i])
    #             dist=fittsData['distance'][i]
    #             width=fittsData['width'][i]
                dist=de
                width=we
                
                #1 is added to calculate the intercept
                X.append([1,np.log2(dist/width+1)])
                
    Y=np.array(Y)
    X=np.array(X)
        
        
    Xt=np.transpose(X)
    IDe=np.log2(dist/width+1)
    c=np.dot(np.dot(np.linalg.inv(np.dot(Xt,X)),Xt),Y)
    print(c)
    IP=1/c[1]
    print('IP %.4f, IDe %.4f'%(IP,IDe))
        
        
        