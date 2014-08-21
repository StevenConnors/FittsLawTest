
import numpy as np
import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
import dataReader as dr
import os
import dataSearchUtils as dS

allFiles= []

tkObj=Tkinter.Tk()
tkObj.file_opt = options = {}

X=[]
Y=[]
  
filesPath=tkFileDialog.askdirectory()

if filesPath:
	for root, dirs, files in os.walk(filesPath):
		for file in files:
			if file.endswith(".dat"):
				 allFiles.append(os.path.join(root, file))

	FileList=[]
	TPList=[]
	IPList=[]
	LinList=[]
	ErrorList=[]
	MTList=[]
	IDeList=[]
	errorRateList=[]
	outlierRateList=[]


	for directory in xrange(len(allFiles)/3):
		
		X=[]
		Y=[]
		averageMT=[]
		allIDe=[]
		TP=0
		errorRate=[]
		aveMt=0
		aveIde=0
		outlierRate=[]
		for someFile in xrange(3):
			file = allFiles[directory*3 + someFile]

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
			
# 			
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

		for j in xrange(3):
			TP+=1.0*allIDe[j]/averageMT[j]
			aveMt+=averageMT[j]
			aveIde+=allIDe[j]
		TP=1.0*TP/3 #div 3 cause the number of files
		
		aveMt=aveMt/3
		aveIde=aveIde/3
		
		head, tail = os.path.split(file)
		head2, target = os.path.split(head)
		ind=dS.strFind(head2,'userData')
		print head2[ind[0]+9:]
		
		target=head2[ind[0]+9:]+"/" +target
		print target
		
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

		FileList.append(target)
		TPList.append(TP)
		ErrorList.append(np.mean(errorRate))
		LinList.append(c)
		IPList.append(IP)
		MTList.append(aveMt)
		IDeList.append(aveIde)
		errorRateList.append(np.mean(errorRate))
		outlierRateList.append(np.mean(outlierRate))

	path="./TPs/"
	savedTitle=path+"allTPs2.dat"
	f=open(savedTitle, 'w')
	f.write("Filename, TP, IP, Lin1, Lin2, ErrorRate, outlierRate, meanMovetime, meanIDe\n")
	for x in xrange(len(TPList)):
# 		stuff = FileList[x]+","+'%.4f'%TPList[x]+","+'%.4f'%IPList[x]+","+'%.4f'%LinList[x][0]+","+'%.4f'%LinList[x][1]+","+'%.4f'%ErrorList[x]\
# 		+","+'%.4f'%MTList[x]+","+'%.4f'%IDeList[x]+","+"\n"
# 		f.write(stuff)
		output='%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f \n'%(FileList[x],TPList[x],IPList[x],LinList[x][0],LinList[x][1],\
														errorRateList[x],outlierRateList[x],MTList[x],IDeList[x])
		f.write(output)
		
	f.close()


