#===============================================================================
# The function in this file calculate different statistics
# and other useful values over data sets
#
# Copyright (C) Julian Ramos 2013
#===============================================================================

#List of functions
#freqs : Counts the frequency of given discrete values on a data vector
#unique : Find the unique values of a data set of discrete values

#===============================================================================
# freqs
# This function searches for a pattern
# in data. Data is a list and pattern is a vector of values this function
# returns a dictionary with the keys indices and counts
#===============================================================================
import numpy as np
import sys
import dataSearchUtils as dataSu

def counts(data):
    
    '''
    Searches through the list of data provided and returns the counts for each of the unique 
    values
    '''
    countsL=[]
    
    vals=unique(data)
    
    for i in vals:
        countsL.append(freqsF(data,i))
        
    return {'counts':countsL,'vals':vals}
    

def freqsF(data,pattern):
    """
      >>> freqsF([1,1,1,1,2],1)
      4
      >>> freqsF([1,1,1,1,2],2)
      1
      >>> freqsF([1,5,5,1,2],5)
      2
      >>> freqsF([1,5,5,1,2],6)
      1
    """
    freqs=list();
    indices=list()
    temp=list()
    results=list()
    
    if type(pattern) is list: 
        if not pattern:
            print('pattern is empty, stopping execution')
            sys.exit()
            
        if type(pattern[0]) is unicode:
            results={}
            for pat in pattern:
                results[pat]=len(dataSu.listStrFind(data,pat))
            return results
        
        if not(type(pattern[0])is int):
            for i in range(0,len(pattern)):
                temp=[item for item in range(len(data)-len(pattern[i])) if data[item:item+len(pattern[i])]==pattern[i]]
                freqs.append(len(temp))
                indices.append(temp)
                
            results={'indices':indices,'counts':freqs}
            return results
        else :
            for i in range(0,len(pattern)):
                indices=[item for item in range(len(data)) if data[item]==pattern[i]]
                freqs.append(len(temp))
                indices.append(temp)
            results={'indices':indices,'counts':freqs}
            return results
#     if type(pattern) is int or type(pattern) is float:
    else:
        return sum([1 for i in data if i==pattern])
            

#===============================================================================
# Unique
# Searches through the data set and returns the unique values 
#===============================================================================

def unique(data):
    seen = list()
    [i in seen or seen.append(i) for i in data]
    return seen


def expSmooth(values,weight):
    """
      >>> expSmooth([1,2,4],0.75)
      3.4375
    """
    last=values[0]
    for i in range(len(values)-1):
        last=values[i+1]*weight+last*(1-weight)
    return last
    



if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    vec=[2,1,3,3,3]
    mx=len(vec)
    cts=counts(vec)
    oCts=sorted(cts['counts'])
#     mx=max(cts['counts'])
    print(oCts)
    print(expSmooth(oCts,0.9)/mx)
    