
import numpy as np
import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
import dataReader as dr
import os
import dataSearchUtils as dS

allFiles= []
output=[]
filename=''
storingPath='/home/julian/Documents/Aptana Studio 3 Workspace/FittsLawTest/summaries/'

tkObj=Tkinter.Tk()
tkObj.file_opt = options = {}

X=[]
Y=[]
  
filesPath=tkFileDialog.askdirectory()

numFiles=0
if filesPath:
      for root, dirs, files in os.walk(filesPath):
          for file in files:
              if file.endswith(".dat"):
                  allFiles.append(os.path.join(root, file))
                  numFiles+=1
      print allFiles    
      
      X=[]
      Y=[]
      averageMT=[]
      allIDe=[]
      TP=0
      errorRate=[]
      outlierRate=[]
      
      
      for file in allFiles:
          #print file
          data=dr.csvReader(file, ',', 4)
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
      #               print(fittsData['movDistance'][i],fittsData['movementTime'][i])
      #               print(meanDe,stdDistance,meanMvt,stdMvt)
                  else:
                      outlier[i]=0
              else:
                  outlier[i]=1
                  
          fittsData['outliers']=outlier
          
          if np.sum(fittsData['wrongClick'])!=0:
                errorRate.append(1.0*np.sum(fittsData['wrongClick'])/len(fittsData['wrongClick']))
          else:
                errorRate.append(0.0)
          
          
          if np.sum(outlier)!=0:
                if fittsData['wrongClick'][0]==1:
                    outlierRate.append(1.0*(np.sum(outlier))/len(outlier)-errorRate[-1])
                else:
                    outlierRate.append(1.0*(np.sum(outlier)-1)/len(outlier)-errorRate[-1])
          else:
                outlierRate.append(0.0)
          
          IDe=[]
          index=[]
          #Fitts law coefficients
          for i in range(len(fittsData['movementTime'])):
              if fittsData['outliers'][i]!=1:
                  
                  Y.append(fittsData['movementTime'][i])
      #             dist=fittsData['distance'][i]
      #             width=fittsData['width'][i]
                  dist=meanDe
                  width=we
                  
                  #1 is added to calculate the intercept
                  X.append([1,np.log2(dist/width+1)])
                  IDe.append(np.log2(dist/width+1))
                  index.append(i)
      
          ##Get the average MT for one round of recording
          MTsum=0
          for i in xrange(len(Y)):
              MTsum+=Y[i]
          MTsum= MTsum/len(Y)
          averageMT.append(MTsum)
          ##Get the average MT for one round of recording
          
          #IDe
          allIDe.append(IDe[0])
          
          inds=dS.strFind(file,'/')
          filename=file[inds[-2]:-4].strip()
          localPath=file[:inds[-1]].strip()
          realWidth=fittsData['width'][0]
          realDistance=fittsData['distance'][0]
          output.append("%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n"%(filename,meanMvt,stdMvt,meanDe,stdDistance,errorRate[-1],\
                                                            outlierRate[-1],IDe[0],width,dist,np.log2(realDistance/realWidth+1),realWidth,realDistance))
          
      
      inds=dS.strFind(localPath,'/')
      folderName=localPath[inds[-1]+1:]
      outputFile='%s%s'%(storingPath,'summary.csv')            
#       outputFile='%s%s%s'%(storingPath,folderName,'_summary.txt')
      with open(outputFile,'w') as ofile:
          ofile.write('filename, meanMT, stdMT, meanDistance, stdDistance, errorRate,'+\
                          'outlierRate, IDe, meanWidth, meanDist,ID,width,distance\n')
          for i in output:
              ofile.write(i)
              
      
      for j in xrange(len(allFiles)):
          TP+=1.0*allIDe[j]/averageMT[j]
      TP=1.0*TP/len(allFiles)
      
      print('Throughput %.4f'%(TP))
      print('Error Rate %.4f'%(np.mean(errorRate)))
      
      Y=np.array(Y)
      X=np.array(X)
      Xt=np.transpose(X)
      
      c=np.dot(np.dot(np.linalg.inv(np.dot(Xt,X)),Xt),Y)
      print "Linear Regression"
      print(c)
      IP=1/c[1]
      print('IP %.4f'%(IP))


        
                
    #Y=np.array(Y)
    #X=np.array(X)
    #Xt=np.transpose(X)
    
    #c=np.dot(np.dot(np.linalg.inv(np.dot(Xt,X)),Xt),Y)
    #print(c)
    #IP=1/c[1]
    #print('IP %.4f'%(IP))
            
    
