#===============================================================================
# The functions in this file are all related with searches in data
#
# Copyright (C) Julian Ramos 2013
#===============================================================================
import sys
import dataStats as dataS



#List of functions
#nlenpatfinder : Pattern search in a vector
#find         : Searches through a vector and return the index of the
#               values fulfilling the condition defined in func 

#===============================================================================
# nlenpatfinder(data,length)
# Searches through data, which is assumed to be a vector,
# for sequential patterns of the size especified by length
#===============================================================================
def nlenpatfinder(data,length):
    tempPat=[data[i:i+length] for i in range(0,len(data)-length+1)]
    tempPat=dataS.unique(tempPat)
    return tempPat
    #print tempPat[len(tempPat)-10:]
    #print data[len(data)-10:]
def flexPatternSearch(data,start,stop):
    '''
    This function searches for a start and stop symbol and gives back the indices where this is found.
    As an example if you have the sequence: 1,2,3,4,5,1,2,7,3
    and you pass start =1 stop =3 then the return indices are
    indicesStart=[0,5]
    indicesStop=[2,8]
    Currently it only works with symbols of size 1, however a list of symbols can be passed too
    >>> a=flexPatternSearch([1,2,3,1,3],1,3)
    >>> a['indicesStart']
    [0, 3]
    >>> a['indicesStop']
    [2, 4]
    '''
    indsStart=[]
    indsStop=[]
    headFound=0
    tempS=0
    for i in range(len(data)):
        if len([ 1 for i2 in range(len(start)) if start[i2]==data[i]])>0:
            tempS=i
            headFound=1
        if len([ 1 for i2 in range(len(stop)) if stop[i2]==data[i]])>0  and headFound==1:
            headFound=0
            indsStart.append(tempS)
            indsStop.append(i)
    return {'indicesStart':indsStart,'indicesStop':indsStop} 
             
    
def find(data,func):
    '''
    def find(data,func):
    This function searches through data which is some iterable data structure like
    list by using func which should be replaced by the next:
    lambda x:x==pattern
    If you want to search for a different condition simply change it to something valid like:
    lambda x:x<pattern
    
    '''
    try :
        return [i for (i, val) in enumerate(data) if func(val)]
    except:
        print('Perhaps you forgot to use lambda x:x==pattern or some other valid expression')
        print('Current program stopped')
        sys.exit()
        
def exactStrFind(data,pattern):
    '''
    Finds a pattern in the iterable data but only returns an index
    if after removing ends of line and spaces it is exactly the same
    as pattern
    '''
    return [i for (i, val) in enumerate(data) if len(val.rstrip())==pattern]

#===============================================================================
# strFind(data,pattern)
# Searches a string data vector for a pattern
#===============================================================================
def strFind(data,pattern):
    res=[i for i in range(len(data)-len(pattern)+1) if data[i:i+len(pattern)]==pattern]
    return res

#===============================================================================
# listStrFind(data,pattern)
# Searches a string data vector for a pattern
#===============================================================================
def listStrFind(data,pattern):
    '''
    This function searches through a list of strings for pattern
    it returns the location in this list where it find pattern
    for the index of where in the string is the pattern
    use strFind
    
    >>> listStrFind(['alas','what is this'],'this')
    [1]
    >>> listStrFind(['alas','what is this alas'],'alas')
    [0, 1]
    '''
    
    return [i for (i, val) in enumerate(data) if val.find(pattern)!=-1]


    
def nonOverlappingSearch(data,pattern):
    i=0
    indices=list()
    while i<=len(data)-len(pattern)+1:
        if data[i:i+len(pattern)]==pattern:
            indices.append(i)
            i=i+len(pattern)
        else:
            i=i+1
    return indices

def findMultiple(data,items):
    '''
    Searches for the items in data, the difference with
    find is that searches for the exact item and also items is
    another list
    '''
    idxs=[]
    for i in items:
        temp=find(data, lambda x:x==i)
        if temp:
            idxs.append(temp[0])
    return idxs
            
        
            

# print [1,2]
# print listStrFind(['alas','what is this alas'],'alas')
if __name__ == "__main__":
    import doctest
    doctest.testmod()