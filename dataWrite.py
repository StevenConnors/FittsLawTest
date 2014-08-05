import numpy as np
import dataOps as dO
from itertools import chain
import csv


def writeLists2csv(*args,**kwargs):
    '''
    This function takes multiple lists and stores them as a csv 
    specified by filename
    '''
    
    
    data=dO.multl2sl(*args)
    
    if 'filename'in kwargs and data:
    
        with open(kwargs['filename'], 'w',newline='') as csvfile:
            doc2write = csv.writer(csvfile, delimiter=',')
            
            if 'header' in kwargs:
                doc2write.writerow(kwargs['header'])
                
            for i in data:
                doc2write.writerow(i)
            return 1
    else:
        print('-->Error')
        print('If not specified above check you are passing a filename')
        return -1
    
def writeLoL2csv(lol,writeState='w',**kwargs):
    '''
    This function takes a list of lists and stores them as a csv 
    specified by filename
    '''
    
    if not np.std([len(lol[i2]) for i2 in range(len(lol))]) == 0:
        print('>>>Error')
        print('lists have different number of elements')
        return None
    data=lol
    #data=[ [lol[i][i2] for i in range(len(lol))] for i2 in range(len(lol[0]))]
    
    if 'filename'in kwargs and data:
    
        with open(kwargs['filename'],writeState,newline='') as csvfile:
            doc2write = csv.writer(csvfile, delimiter=',')
            
            if 'header' in kwargs:
                doc2write.writerow(kwargs['header'])
                
            for i in data:
                doc2write.writerow(i)
            return 1
    else:
        print('-->Error')
        print('If not specified above check you are passing a filename')
        return -1

def writeDoL2csv(lol,**kwargs):
    '''
    This function takes a dictionary of lists and stores them as a csv 
    specified by filename
    '''
    
    if not np.std([len(lol[i2]) for i2 in lol]) == 0:
        print('>>>Error')
        print('lists have different number of elements')
        return None
    
#     data=[ [lol[i][i2] for i in range(len(lol))] for i2 in range(len(lol[0]))]
#     data=[[i2 for i2 in range(len(lol[i]))] for i in lol]


    dKeys=lol.keys()
    data=[[lol[i2][i] for i2 in lol.keys() ]for i in range(len(lol[dKeys[0]]))]

    
    if 'filename'in kwargs and data:
    
        with open(kwargs['filename'], 'w',newline='') as csvfile:
            doc2write = csv.writer(csvfile, delimiter=',')
            
            if 'header' in kwargs:
                doc2write.writerow(kwargs['header'])
            else:
                header=[i for i in lol]
                doc2write.writerow(header)
                
            for i in data:
                doc2write.writerow(i)
            return 1
    else:
        print('-->Error')
        print('If not specified above check you are passing a filename')
        return -1





if __name__=='__main__':
    
    x = ['a','b','c','d','e','f']
    y = ['1','2','3','4','5','6']
    x2 = ['e','r','t','y','u']
    a=[[1,2]]*10
    
    print('Correct output')
    print(writeLists2csv(x,y,x,filename='test.csv'))
    print('Incorrect output')
    print(writeLists2csv(x,y,x2,x,filename='test.csv'))
    print(a)
    print(writeLoL2csv(a,filename='test.csv'))
    
