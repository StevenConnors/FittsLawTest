'''
This set of functions are specialized Ml algorithms for big data sets 
where the computing is done on chunks of data
by Julian Ramos
'''

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


def partialFitMiniBatchKmeans(training_file,categorical_features,label,maxLines,ks):
    stop=False
    cont=0
    km=[]
    with open(training_file,'r') as f:
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
                        km=MiniBatchKMeans(init='k-means++', n_clusters=ks, batch_size=len(data),
                                n_init=10, max_no_improvement=10, verbose=0)
                        km.partial_fit(data)
    return km
            
def partialCLF(clf,train_file,test_file,label_idx,categorical_vars,maxLines=1000):
    '''
    categorical_vars refers to the variables that are categorical in the
    data set. For them since I will be using regression I can simply
    convert this to dummys
    Also, I should normalize all of the data, it is quite a mess right now
    even though they said they had standardized the values it is not really 
    quite like that
    Also I have to make the loss label into a 0 1 thing
    This function stills needs work
    '''
    if clf == 'logistic':
        clf=lm.LogisticRegression(penalty='l1',class_weight='auto')
    stop=False
    
    #First determining the categorical variables range and creating dummies
    with open(train_file,'r') as f:
        data=[]
        NAs=[]
        header=f.readline().split(',')
        catIdxs=dSu.findMultiple(header, categorical_vars)
        cont=0
        while stop==False:
            stop=True
            for i in f:
                stop=False
                cont+=1
                temp=i.split(',')
                temp=np.array([float(i2) for i2 in temp])
                data.append(temp[catIdxs])
                if cont==maxLines:
                    break
    data=np.array(data)        
    unique=np.unique(data)
    print(unique)
                
    


    with open(train_file,'r') as f:
        while stop==False:
            data=[]
            NAs=[]
            header=f.readline().split(',')
            catIdxs=dSu.findMultiple(header, categorical_vars)
            cont=0
            stop=True
            for i in f:
                stop=False
                cont+=1
                temp=i.split(',')
                temp=[float(i2) for i2 in temp]
                data.append(temp)
                if cont==maxLines:
                    break
            clf.partial_fit()