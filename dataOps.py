#===============================================================================
# The functions in this file perform differnt data operations over lists
#
# Copyright (C) Julian Ramos 2013
#===============================================================================
import numpy as np
import time
import datetime
import numpy as np
import dataSearchUtils as dataS
import matplotlib.pyplot as plt
import pytz

def deleteStrInds(data,inds):
    '''
    def deleteStrInds(data,inds):
    This function searches through the data and eliminates the indexes in inds
    to avoid problems it goes from the least item to the first
    Also the inds are sorted to prevent erasing earlier in the list items
    that cause to erase by mistake later items
    >>> a='asd,asd,asd,123,asd,'
    >>> inds=[3,7,11]
    >>> deleteStrInds(a,inds)
    'changes done directly on the input str'
    >>> print a
    'asdasdasd123,asd,'
    '''
    inds=sorted(inds)
    temp=''
    for i in range(len(data)-1,-1,-1):
        if len(dataS.find(inds,lambda x:x==i))>0:
            pass
        else:
           temp='%s%s'%(data[i],temp)
    
            
    return temp

    
def deleteInds(data,inds):
    '''
    def deleteInds(data,inds):
    This function searches through the data and eliminates the indexes in inds
    to avoid problems it goes from the least item to the first
    Also the inds are sorted to prevent erasing earlier in the list items
    that cause to erase by mistake later items
    >>> a=[1,2,3,4,5,6,7,8,9,1,2,3,4,1,2,3,4,5]
    >>> inds=[10,1,3]
    >>> deleteInds(a,inds)
    'changes done directly on the input list'
    >>> print a
    [1, 3, 5, 6, 7, 8, 9, 1, 3, 4, 1, 2, 3, 4, 5]
    '''
    inds=sorted(inds)
    for i in range(len(data)-1,-1,-1):
        if len(dataS.find(inds,lambda x:x==i))>0:
            data.pop(i)
            
    return 'changes done directly on the input list'
    
#     dataout=[data[i] for i in range(len(data)-1,-1,-1) if len(dataS.find(inds,lambda x:x==i))==0]
#     return dataout
    #getvar=lambda searchList, ind: [searchList[i] for i in ind if len(dataS.find(ind,ind==i))==0]
    #return getvar(data,inds)
    
#    fromApptoCode(data):
#    This function changes the symbols in the list to 
#    codes and returns both the codes and the data set
#    changed to the codes representation
def fromApptoCode(data):
    appsList=list()
    newData=list()
    for i in range(len(data)):
        inds=dataS.find(appsList, lambda x:x==data[i])
        if len(inds)!=0:
            newData.append(inds)
        else:
            appsList.append(data[i])
            inds=dataS.find(appsList, lambda x:x==data[i])
            newData.append(inds)
    return [newData,appsList]



#function time2vec=timevectransform(timestamps)
#This function takes the timestamps data and transforms in a way that
#geomatrically the measurements between values will correspond to those of
#the time format. As an example: the difference in hours between 22 and 1
#is actually is 3 hours and not 21 which will be the regular difference.
#Instead what we can do is map the hours values to a circle coordinates.
#To find the equivalency we simply have two tables one with the circle
#coordinates and the other with the hours. We do not explicitely create a
#function but instead look at the hours equivalent for each value. This
#trick is useful when you want to try to do clustering and you cannot
#use a custom made distance metric. In that case you could use the
#euclidean and this transformation and it will work approximately like
#using a special distance for the time.

def time2vec(timestamps):    
    time2vec.x=np.array([])
    time2vec.y=np.array([])
    time2vec.z=np.array([])
    
    if len(time2vec.x)==0 and len(time2vec.y)==0 and len(time2vec.z)==0:
        r=5
        step=0.001
        theta=np.arange(0,np.pi*2,step)
        
#        time2vec.x=[r*np.cos(i) for i in theta]
        time2vec.x=-r*np.cos(theta)
        time2vec.y=r*np.sin(theta)
#        time2vec.y=[r*np.sin(i) for i in theta]
        
        step2=24./len(theta)
        time2vec.z=np.arange(0,24,step2)
#        plt.plot(time2vec.x,'r')
#        plt.plot(time2vec.y,'b')
#        plt.plot(time2vec.z,'k')
#        plt.scatter(time2vec.x,time2vec.y)
        
#        plt.show()

#    plt.scatter(time2vec.x, time2vec.y)
#    plt.show()
#        
    #Changing from minutes to a scale that goes between 0 to 99
#    print(datetime.datetime.fromtimestamp(int(timestamps)).strftime('%Y-%m-%d %H:%M:%S'))
    hours=[int(datetime.datetime.fromtimestamp(int(i)).strftime('%H')) for i in timestamps]
    minutes=[int(datetime.datetime.fromtimestamp(int(i)).strftime('%M')) for i in timestamps]
#     print hours[1:10]
#     print minutes[1:10]
    
    timeDec=[hours[i]+np.divide(int(minutes[i]),60.) for i in range(len(timestamps))]
#     print timeDec[1:10]
    timevec=list()
#    print time2vec.x.size
#    print time2vec.y.size
#    print time2vec.z.size
    
    for i in timeDec:
        ind=np.argmin(np.abs(time2vec.z-i));
        timevec.append([time2vec.x[ind], time2vec.y[ind]])
#        
#    X=[i[0] for i in timevec]
#    Y=[i[1] for i in timevec]
#    plt.plot(X,Y)
#    plt.show()

    return timevec
  
 
#timestamps=[1341884014,1341884014,1341884014,1341884014,1341884014,1341884014,1341884014]
#time2vec(timestamps)   


def time2dec(timeData,basis,**kwargs):
    if 'timezone' in kwargs:
        tz=kwargs['timezone']
    else :
        tz='Asia/Seoul'
    print('This function is currently using Seoul\'s time zone when no other time zone is provided')
    H=np.array([ int(datetime.datetime.fromtimestamp(int(i),tz=pytz.timezone(tz)).strftime('%H')) for i in timeData])
    M=np.array([ int(datetime.datetime.fromtimestamp(int(i),tz=pytz.timezone(tz)).strftime('%M')) for i in timeData])
    S=np.array([ int(datetime.datetime.fromtimestamp(int(i),tz=pytz.timezone(tz)).strftime('%S')) for i in timeData])
    
#   H=np.array([ int(datetime.datetime.fromtimestamp(int(i),tz=pytz.timezone('Asia/Seoul')).strftime('%H')) for i in timeData])
#   M=np.array([ int(datetime.datetime.fromtimestamp(int(i)).strftime('%M')) for i in timeData])
#   S=np.array([ int(datetime.datetime.fromtimestamp(int(i)).strftime('%S')) for i in timeData])
#   dates=[ datetime.datetime.fromtimestamp(int(i)).strftime('%Y-%m-%d %H:%M:%S') for i in timeData]
    
    D=[datetime.datetime.fromtimestamp(int(i)).weekday() for i in timeData]    
    
    if basis=='Daily':
        dec=np.int_(H)+np.int_(100*M/60.0)/100.0+ np.int_(100*S/60.0)/10000.0
    if basis=='Weekly':
        dec=D+np.int_(100*H/24.0)/100.0+np.int_(100*M/60.0)/10000.0+ np.int_(100*S/60.0)/1000000.0
    if basis=='Hourly':
        dec=np.int_(M)+ np.int_(100*S/60.0)/100.0
#     dec=np.int_(100*H/24.0)/100.0+np.int_(100*M/60.0)/10000.0+ np.int_(100*S/60.0)/1000000.0

    return dec


def data2csv(filein,fileout,delimiters):
    '''
    def data2csv(filename):
    This function transforms the input data set defined by filein to a comma separated file fileout
    using the delimiters specified.
    
    The delimiters should passed as a list, as an example:
    
    delimiters=[',','\t', '|']
    '''
    
    fout=open(fileout,'w')
    if fout==-1:
        print('Could not create the output file')
    print('Starting conversion operation for '+filein)
    with open(filein,'r') as f:
        for line in f:    
            for di in delimiters:
                line=line.replace(di,',')
            line=line.replace(',,,,,',',')
            line=line.replace(',,,,',',')
            line=line.replace(',,,',',')
            line=line.replace(',,',',')
            if line[-2]==',':
                line=line[0:-2]
            #If the end of the line does not have a newline just add it
            if str(line[-1:])!=str('\n'):
                line=line+str('\n')
            fout.write(line)
    fout.close()
    print('Conversion done')

    
    
def multl2sl(*args):
    '''
    This function takes all the input lists and transform it to a
    single list
    '''
    superList=[]
    cols=len(args)
    rows=len(args[0])
    
    
    if np.std([len(args[i]) for i in range(cols)]) != 0:
        print('the number of rows is not the same accross lists')
        return None
    
    superList=[[ args[i][i2] for i in range(cols)] for i2 in range(rows)]
#     for i2 in range(rows):
#         temp=[]
#         for i in range(cols):
#             temp.append(args[i][i2])
#         superList.append(temp)
    return superList
     
def minimum(data):
    col=np.argmin(np.min(data,axis=0))
    row=np.argmin(data[:,col])
    return {'row':row,'col':col,'val':data[row,col]}
    
def maximum(data):
    col=np.argmax(np.max(data,axis=0))
    row=np.argmax(data[:,col])
    return {'row':row,'col':col,'val':data[row,col]}

def timestamp2Str(timestamp,**kwargs):
        
    #Using the desktop's local time zone
    
     
    Y=datetime.datetime.fromtimestamp(timestamp).strftime('%Y')
    m=datetime.datetime.fromtimestamp(timestamp).strftime('%m')
    d=datetime.datetime.fromtimestamp(timestamp).strftime('%d')
    H=datetime.datetime.fromtimestamp(timestamp).strftime('%H') 
    M=datetime.datetime.fromtimestamp(timestamp).strftime('%M') 
    S=datetime.datetime.fromtimestamp(timestamp).strftime('%S') 
    F=datetime.datetime.fromtimestamp(timestamp).strftime('%f') 
    
    return Y+'/'+m+'/'+d+'/'+H+'/'+M+'/'+S+'/'+F

def str2timestamp(timestamp,**kwargs):
    if 'timezone' in kwargs:
        tz=kwargs['timezone']
    else :
        tz='UTC'
        print('Using the default time zone UTC')
#     return datetime.datetime.strptime(timestamp, "%H:%M:%S:%f").timetuple()
    return time.mktime(datetime.datetime.strptime(timestamp,"%H:%M:%S:%f").timetuple())

def appendDicts(dictA,dictB):
    '''
    This function takes two dictionaries with the same
    keys and append their contents into one new dictionary.
    The function assumes the values for the keys are lists
    '''
    if type(dictA) is list:
        dictA=dictA[0]
    if type(dictB) is list:
        dictB=dictB[0]
        
    
    dictC=dictB
    for i in dictA.keys():
        dictC[i]+=dictA[i]
        
    return dictC

def incompDate2timestamp(dateStr,timestamp,**kwargs):
    '''
    Creates a timestamp from an incomplete date. Date has information 
    about the Hour, minute, second and millisecond only. 
    '''
    baseDate=timestamp2Str(timestamp).split('/')
    partialStr=baseDate[0]+'/'+baseDate[1]+'/'+baseDate[2]+'/'
    
    if 'irregular' in kwargs:
        temp2=dateStr.split(':')
        if int(temp2[0])<9:
            temp2[0]=str(int(temp2[0])+12)
        dateStr=':'.join(temp2)
    
    date2=time.mktime(datetime.datetime.strptime(partialStr+dateStr, "%Y/%m/%d/%H:%M:%S:%f").timetuple())
    temp=dateStr.split(':')
    return {'timestamp':date2,'milliseconds':int(temp[-1]),'milliTimestamp':date2+int(temp[-1])/float(1000)}
    
        
#===============================================================================
# #Test data2csv    
# data2csv('K:/research_data_sets/Activity recognition study/S03_1/1360681304.dat','K:/research_data_sets/Activity recognition study/S03_1/1360681304.csv',['\t',' ',',','|','#',';'])
#===============================================================================
if __name__ == "__main__":
    import doctest
    timestamps=[]
    for i in range( 1405296000 ,  1405382399 ,3600):
        timestamps.append(i)
    coords=time2vec(timestamps)
    X=[i[0] for i in coords]
    Y=[i[1] for i in coords]
    plt.plot(X,Y,'o')
    plt.show()
    
#     print(time2vec([1405363573]))
#     print(time2vec([1405376269]))
    doctest.testmod()