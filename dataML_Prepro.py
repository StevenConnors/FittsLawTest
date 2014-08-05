'''
Created on Feb 13, 2014
This set of functions are for preprocessing of data sets
for the dataML_big
@author: julian
'''
#import General as gf
import unittest
import dataWrite as dW
import pickle
import numpy as np
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_score as silhouette
import dataSearchUtils as dSu
import scipy.spatial.distance as distance
import sklearn.linear_model as lm
from sklearn import cross_validation
import os


def crossvalidationSPF(trainFile,data_path,folds):
    '''
    This function takes a training file and splits it into training
    and testing data sets that are stored under a folder called temp
    in the data path provided. The number of files depends on the folds provided
    '''
    #All this section should be a function
    with open(trainFile,'r') as f:
        data=[]
        for line in f:
            data.append(line)
    temp_path=data_path+'temp_cv'
    try: 
        os.mkdir(temp_path)
    except:
        print('folder already exists, will not create crossvalidation files')
        files=os.listdir(temp_path)
        idx=dSu.listStrFind(files, 'train')
        training_files=[ temp_path+'/'+files[i] for i in idx]
        idx=dSu.listStrFind(files, 'test')
        testing_files=[ temp_path+'/'+files[i] for i in idx]
        return training_files,testing_files
        
    #Drop the header
    header=data.pop(0)
    
    #Create the crossvalidation files
    kf=cross_validation.KFold(len(data),n_folds=folds)
    cont=1
    
    training_files=[]
    testing_files=[]
    for traf,tesf in kf:
        temp_train_filename=temp_path+'/'+'cv_train%d.csv'%(cont)
        temp_test_filename=temp_path+'/'+'cv_test%d.csv'%(cont)
        cont+=1
        temp_file=open(temp_train_filename,'w')
        training_files.append(temp_train_filename)
        temp_file.write(header)
        for i in traf:
            temp_file.write(data[i])
        temp_file.close()
        temp_file=open(temp_test_filename,'w')
        testing_files.append(temp_test_filename)
        temp_file.write(header)
        for i in tesf:
            temp_file.write(data[i])
            
    print('Kfold-crossvalidation files stored')
    print(training_files)
    print(testing_files)
    
    return training_files,testing_files
        
def missingEM(filename,temp_path,maxK,categorical_features,label,kfolds=2):
    '''
    This function uses EM to fill in missing values in a data set. 
    First it calculates mini-batch kmeans on the data set without
    the missing data. This is done in crossvalidation fashion so that the best
    k can be selected. Once the best k is selected a new kmeans model is estimated
    once the centroids are obtained, the values replace accordingly the missing data
    '''
    #Values higher than this will cause the silhouette to run too slow
    #I should probably modify the silhouette
    #Currently it is not very well implemented
    #Just the average is actually wrong
    #Also remember about the gap statistics
    #Maybe I should implement it
    
    maxLines=1000
    
    filesList=os.listdir(temp_path)
    if dSu.listStrFind(filesList, 'meanSils') ==[]:
        print('Pickle not found starting the crossvalidated EM to determine number of K')
        training_files,testing_files=crossvalidationSPF(filename,temp_path,kfolds)
        meanSils=[[0 for i2 in range(kfolds)]for i in range(0,maxK)]
        for fId in range(len(training_files)):
            data=[]
            km=[[]for i in range(maxK)]
            sils=[[] for i in range(maxK)]
            #Training section for all of the data files
            #In this section we get the kmeans models
            #For all of the different k's once we get all of the models
            #We get the silhouette score on the 
            #testing data
            cont=0
            stop=False
            with open(training_files[fId],'r') as f:
                while stop==False:
                    print('Training section - reading data from file ...')
                    if cont==0:
                        header=f.readline().rstrip().split(',')
                        idx=dSu.findMultiple(header, categorical_features)
                        idx+=dSu.listStrFind(header,label)
                    cont+=1
                    
                    data=[]
                    stop=True
                    print(cont)
                    for line in f:
                        stop=False
                        temp=line.rstrip().split(',')
                        if dSu.listStrFind(temp,'NA')==[]:
                            temp=[float(temp[i]) for i in range(len(temp)) if not i in idx]
                            data.append(temp)
                        if len(data)==maxLines:
                            break
                    if stop==False:
                        for kId in range(2,maxK):
                            if km[kId]==[]:
                                km[kId]=MiniBatchKMeans(init='k-means++', n_clusters=kId, batch_size=len(data),
                                n_init=10, max_no_improvement=10, verbose=0)
                            km[kId].partial_fit(data)
                        
    #                 print('Adding the next piece of code to terminate early')
    #                 break
                
                #Testing section
                #Here now that we have the models we simply test them
                #however we store the values and later we average them
            print(temp)
            cont=0
            stop=False
            with open(testing_files[fId],'r') as f:
                while stop==False:
                    print('Testing section reading data from file ...')
                    if cont==0:
                        header=f.readline().rstrip().split(',')
                        idx=dSu.findMultiple(header, categorical_features)
                        idx+=dSu.listStrFind(header,label)
                    cont+=1
                    data=[]
                    stop=True
                    for line in f:
                        stop=False
                        temp=line.rstrip().split(',')
                        if dSu.listStrFind(temp,'NA')==[]:                
                            temp=[float(temp[i]) for i in range(len(temp)) if not i in idx]
                            data.append(temp)
                        if len(data)==maxLines:
                            break
                    if stop==False:
                        for kId in range(2,len(km)):
                            labels=km[kId].predict(data)
                            print('Computing silhouette for %d'%(kId))    
                            sils[kId].append(silhouette(data,labels,metric='correlation'))
    #                 print('Adding the next piece of code to terminate early')
    #                 break
                
            
            for kId in range(2,len(km)):
                meanSils[kId][fId]=np.mean(sils[kId])
        print(meanSils)
        pickle.dump(meanSils,open(temp_path+'/'+'meanSils','wb'))
        print('remember the resulst where stored in %s'%(temp_path+'/'+'meanSils'))
        print('kmean models built')
    elif dSu.listStrFind(filesList, 'meanSils') !=[]:
        print('A pickle meanSils was found in %s, proceeding with the missing data imputation'%(temp_path))
        meanSils=pickle.load(open(temp_path+'/'+'meanSils','rb'))
        meanSils=np.array(meanSils[2:][:])+1
        aveMeanSils=np.mean(meanSils,1)
        ind=np.argmax(aveMeanSils)
        k=ind+2
        print('The best k is %d'%(k))
        #In the next section I build the Kmeans model using all of the training data available
        #it does not matter that is not crossvalidated or anything like that
        cont=0
        stop=False
        kmns=partialFitMiniBatchKmeans(filename,categorical_features,label,maxLines,k)
        with open(filename,'r') as f:
                while stop==False:
                    print('Imputing missing data')
                    data=[]
                    
                    if cont==0:
                        header=f.readline().rstrip().split(',')
                        #here I'm adding the categorical features ids
                        #so that later I do not consider them
                        #however I have to later add them back to the data once
                        #the missing imputation has been worked out
                        #hence there is probably no need to remove 
                        #this from the header
                        #also finish checking that the data is being stored
                        #correctly before moving forward
                        
                        idx=dSu.findMultiple(header, categorical_features)
                        idx+=dSu.listStrFind(header,label)
                        data=[header]
                    cont+=1
                    stop=True
                    print(cont)
                    for line in f:
                        stop=False
                        temp=line.rstrip().split(',')
                        temp=[temp[i] for i in range(len(temp)) if i not in idx]
                        if dSu.listStrFind(temp,'NA'):
                            vec=[ [int(key),float(val)] for (key,val) in enumerate(temp) if val!='NA']
                            vecs=np.array([i[1] for i in vec])
                            idVec=[i[0] for i in vec]
                            cents=kmns.cluster_centers_
                            dist=[]
                            for i in range(np.shape(cents)[0]):
                                tempVec=[ cents[i,i2] for i2 in idVec]
                                dist.append(distance.euclidean(tempVec,vecs))
                            ind=np.argmin(dist)
                            
                            #Now replacing here the missing data
                            inds=dSu.listStrFind(temp, 'NA')
                            for i in inds:
                                temp[i]=str(cents[ind,i])
                            #Adding the categorica data back
                            for i in idx:
                                lineTemp=line.rstrip().split(',')                                
                                temp.insert(i,lineTemp[i])
                            data.append(temp)
                        else:
                            #Adding the categorica data back
                            for i in idx:
                                lineTemp=line.rstrip().split(',')                                
                                temp.insert(i,lineTemp[i])
                            data.append(temp)
                            
                        if len(data)==maxLines:
                            #Here I have to write or append to a file the array data
                            #file=open(filename[:-4]+'noNA.dat','a')
                            if cont==1:
                                writeState='w'
                            else:
                                writeState='a'
                            dW.writeLoL2csv(data,filename=filename[:-4]+'noNA.csv', writeState=writeState)
                            break
                    #Erase this braek later
                    #break
        print('Imputed missing data')
        print('Files with the extension -noNA.csv where added to your working folder')
        
        
        
def dataSplitBalancedClass(data,labels,rand=True):
    '''
    This function divides the data into testing, validation and training data sets
    while preserving the ratios between data points accross classes
    the optional argument rand specifies whether the data set should be randomly
    shuffled and from it divide into testing validation and training data sets
    '''

    trainData=[]
    testData=[]
    valData=[]
    
    trainLabels=[]
    testLabels=[]
    valLabels=[]
    
    #Checking the type of data is np.array else changinig it
    #to numpy array
    if type(data)!= type(np.array([])):
        data=np.array(data)
     
    #Randomly shuffling the data
    #while preserving the right labels   
    if rand==True:
        inds=np.arange(len(data))
        np.random.shuffle(inds)
        data=data[inds]
        labels=labels[inds].ravel()
        
    
        
    numClasses=np.unique(labels)
    
    for classInd in numClasses:
        inds=np.argwhere(labels==classInd).ravel()
        chunkS=len(inds)/3
        trainInds=inds[0:chunkS]
        testInds=inds[chunkS:chunkS*2]
        valInds=inds[chunkS*2:]
        
        #This data appending is wrong both for the labels and the data
        #reason is that it is appending individual vectors I should use a horcat
        #or vercat! or I can 
        #make it later into a flat vector instead
        
        #Assigning data
        if trainData==[]:
            trainData=data[trainInds]
            trainLabels=labels[trainInds]
        else:
            trainData=np.vstack((trainData,data[trainInds]))
            trainLabels=np.hstack((trainLabels,labels[trainInds]))
            
        if testData==[]:
            testData=data[testInds]
            testLabels=labels[testInds]
        else:
            testData=np.vstack((testData,data[testInds]))
            testLabels=np.hstack((testLabels,labels[testInds]))
            
        if valData==[]:
            valData=data[valInds]
            valLabels=labels[valInds]
        else:
            valData=np.vstack((valData,data[valInds]))
            valLabels=np.hstack((valLabels,labels[valInds]))
        
    
    
        
    trainData=np.array(trainData)
    testData=np.array(testData)
    valData=np.array(valData)
    
    
                             
    return {'trainData':trainData,'testData':testData,'valData':valData,'trainLabels':trainLabels,'testLabels':testLabels,'valLabels':valLabels}

#The next is simply a test unit that tests the dataSplitBalancedClass function
class dataSplitRatioPreservingTest(unittest.TestCase):
    def test_ratio(self):
        #Generate random data
        data=np.random.rand(45,1)
        #Classes for the data, the repetition of a class here
        #changes the ratio of the class labels in the data
        classes=[1,2,3,3,4,4,4]
        uniqueClasses=np.unique(classes)
        numClasses=len(uniqueClasses)
        #The labels are assigned drawing randomly from classes
        #notice how depending the way classes data are distributed
        #changes the ratios between classes
        labels=np.random.choice(classes,len(data))
        dataOut=dataSplitBalancedClass(data,labels,rand=True)
        
        dataTrain=dataOut['trainData']
        dataTest=dataOut['testData']
        dataVal=dataOut['valData']
        
        labelsTrain=dataOut['trainLabels']
        labelsTest=dataOut['testLabels']
        labelsVal=dataOut['valLabels']
        
        
        #Here we are going to calculate the real ratio between classes:
        compOrig=np.array(np.zeros((numClasses,numClasses)))
        for i,val in enumerate(uniqueClasses):
            for i2,val2 in enumerate(uniqueClasses):
                compOrig[i,i2]=len(np.argwhere(classes==val))/float(len(np.argwhere(classes==val2)))
        
        #Here we are going to calculate the average ratio between classes for the shuffled data
        comp=np.array(np.zeros((numClasses,numClasses)))
        for i,val in enumerate(uniqueClasses):
            for i2,val2 in enumerate(uniqueClasses):
                comp[i,i2]=len(np.argwhere(labelsTrain==val))/float(len(np.argwhere(labelsTrain==val2)))+\
                            len(np.argwhere(labelsTest==val))/float(len(np.argwhere(labelsTest==val2)))+\
                            len(np.argwhere(labelsVal==val))/float(len(np.argwhere(labelsVal==val2)))
                comp[i,i2]=comp[i,i2]/float(3)
                
        
        
        #The comparisson of ratios it is not going to give the
        #exact equal ratios but it should be a close value
        error=np.abs(compOrig-comp)
        print('Error ratio matrix')
        print(error)
        print('Mean ratio error')
        print(np.mean(error))
        self.assertTrue(np.mean(error)<1)
#         self.assertEqual(originalRatios,outputRatios)

if __name__=='__main__':
    unittest.main()
    