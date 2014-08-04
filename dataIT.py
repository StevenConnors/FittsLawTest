import numpy as np
import dataStats as dataS
from itertools import izip
import scipy as sp

#===============================================================================
# editD(strng1,strng2):
# This function computes the edit distance between two strings
#===============================================================================
def editD(strng1,strng2):
    m=len(strng1);
    n=len(strng2);
    v=np.zeros((m+1,n+1),dtype=int)

#     print '%d %d'%(m,n)
    for i in range(m+1):
        v[i][0]=i
        
    for j in range(n+1):
        v[0][j]=j

    for i in range(m):
        for j in range(n):
#            print strng1[i]
#            print strng2[j]
            if strng1[i] == strng2[j]:
                v[i+1][j+1]=v[i][j];
            else:
                v[i+1][j+1]=1+np.minimum(np.minimum(v[i+1][j],v[i][j+1]),v[i][j]);
        
    return np.float(v[m][n]);

#===============================================================================
# similarity(strng1,strng2):
# Return the similarity which is simply 1- the edit distance
#===============================================================================
def similarity(strng1,strng2):
#     print editD(strng1,strng2)
#     print np.maximum(len(strng1),len(strng2))
#     print (editD(strng1,strng2)/np.maximum(len(strng1),len(strng2)))
#     print np.float(editD(strng1,strng2))/np.float(np.maximum(len(strng1),len(strng2)))
    return 1-(editD(strng1,strng2)/np.maximum(len(strng1),len(strng2)))

# print editD('lame','loma')
# print np.zeros((3,1))
# print similarity('lame','lamesi')
#print editD('alames','lam')
#print editD([101,101,114,111,103],[114,111])


def entropy(data):
    #This function calculates the entropy of a lists of observations
    if type(data) is list:
        data=dlist2slist(data)
        contents=dataS.unique(data)
        counts=[dataS.freqsF(data, np.asscalar(np.int16(i))) for i in contents]
#         if not(type(counts[0]) is int):
#             print 'error'
        counts=np.array(counts)
        probs=np.double(counts)/np.sum(counts)
        if np.size(probs)!=1:
            return np.sum([-i*np.log(i)/np.log(len(probs)) for i in probs])
        else:
            return 0
    else:
        print 'dataIT->entropy: Unsupported data type\n Only lists supported right now' 
                
def informationContent(data):
    #This function calculates the information content from a list of observations
    #Information content here is simply a modification of shanon's entropy
    if type(data) is list:
        if len(data) <=1:
#             print 'List is empty or doesn\'t have enough elements'
            return 0
        
#     if not(type(data) is list and type(data[0])is list):
#         return 0
        
    return np.around((np.tanh( (entropy(data)-0.8)*20)+1)/2,decimals=4)
    
def dlist2slist(data):
    
    if type(data) is list and type(data[0])is list:
#         print [i[0] for i in data]
        return [i[0] for i in data]
    elif type(data) is list and (type(data[0])is int or type(data[0])is np.int32):
        return data
    else:        
        print '>>>Error dataIT-> dlist2slist : data is not a list of lists'
        
def entropyFromProbs(probs):
    probs=list(probs)
    return np.sum([-i*np.log(i)/np.log(len(probs)) for i in probs])
    


"""
Algorithms on entropies.
"""


def get_base(unit ='bit'):
    if unit == 'bit':
        log = sp.log2
    elif unit == 'nat':
        log = sp.log 
    elif unit in ('digit', 'dit'):
        log = sp.log10  
    else:
        raise ValueError('The "unit" "%s" not understood' % unit)
    return log

def shannon_entropy(freq, unit='bit'):
    """Calculates the Shannon Entropy (H) of a frequency.
    
    Arguments:
    
        - freq (``numpy.ndarray``) A ``Freq`` instance or ``numpy.ndarray`` with 
          frequency vectors along the last axis.
        - unit (``str``) The unit of the returned entropy one of 'bit', 'digit' 
          or 'nat'.
    """
    log = get_base(unit)
    shape = freq.shape # keep shape to return in right shape
    Hs = np.ndarray(freq.size / shape[-1]) # place to keep entropies
    # this returns an array of vectors or just a vector of frequencies
    freq = freq.reshape((-1, shape[-1])) 
    # this makes sure we have an array of vectors of frequencies
    freq = np.atleast_2d(freq)
    # get fancy indexing
    positives = freq != 0.
    for i, (freq, idx) in enumerate(izip(freq, positives)):
        freq = freq[idx] # keep only non-zero
        logs = log(freq) # logarithms of non-zero frequencies
        Hs[i] = -np.sum(freq * logs)
    Hs.reshape(shape[:-1])
    return Hs
 
def relative_entropy(freq, background, unit='bit'):
    """
    Calculates the Releative Entropy (D), which is the Kullback-Leibler 
    divergence between two frequencies. The two arrays "freq" and "background"
    need to broadcast to a single shape. 
    
    Arguments:
    
        - freq (``numpy.ndarray``) A ``Freq`` instance or ``numpy.ndarray`` with
          frequency vectors along the last axis.
        - background (``numpy.ndarray``) ``Freq`` instance or ``numpy.ndarray`` 
          with frequency vectors along the last axis. This typically is a 
          rank-1 array.
          
    Could be normalized?: Dkl = Dkl / log(len(background))
    """
    log = get_base(unit)
    shape = freq.shape
    freq = freq.reshape((-1, shape[-1]))  
    freq = np.atleast_2d(freq) 
    Dkls = np.ndarray(freq.size / shape[-1])
    positives = (freq != 0.) & (background != 0.)
    for i, (freq, idx) in enumerate(izip(freq, positives)):
        freq = freq[idx]
        bg = background[idx]
        logs = log(freq / bg)
        Dkls[i] = np.sum(freq * logs)
    Dkls.reshape(shape[:-1])
    return Dkls

def mutual_information(jointfreq, rowfreq=None, colfreq=None, unit='bit'):
    """
    Calculates the Mutual Information (I) of a joint frequency. The marginal
    frequencies can be given or are calculated from the joint frequency.
    
    Arguments:
    
        - jointfreq (``numpy.ndarray``) A normalized ``JointFreq`` instance or
          ``numpy.ndarray`` of rank-2, which is a joint probability distribution
          function of two random variables.
        - rowfreq (``numpy.ndarray``) [default: ``None``] A normalized marginal 
          probability distribution function for the variable along the axis =0. 
        - colfreq (``numpy.ndarray``) [default: ``None``] A normalized marginal 
          probability distribution function for the variable along the axis =1.
        - unit (``str``) [defualt: ``"bit"``] Unit of the returned information.   
    """
    log = get_base(unit)
    rowfreq = rowfreq or np.sum(jointfreq, axis=1)
    colfreq = colfreq or np.sum(jointfreq, axis=0)
    indfreq = np.dot(rowfreq[None].transpose(), colfreq[None])
    non_zero = jointfreq != 0.
    jntf = jointfreq[non_zero]
    indf = indfreq[non_zero]
    return np.sum(jntf * log(jntf/indf))

def jensen_shannon_divergence(freq, weights =None, unit='bit'):
    """
    Calculates the Jensen-Shannon Divergence (Djs) of two or more frequencies.
    The weights are for the relative contribution of each frequency vector. 
    
    Arguments:
    
        - freq (``numpy.ndarray``) A ``Prof`` instance or a rank-2 array of 
          frequencies along the last dimension.
        - weights (``numpy.ndarray``) An array with a weight for each 
          frequency vector. Rank-1.
        - unit (``str``) see: the function ``shannon_entropy``.
    """
    if weights is not None:
        if len(freq) != len(weights):
            raise ValueError('The number of frequencies and weights do not match.')
        if (freq.ndim != 2) or (len(freq) < 2):
            raise ValueError('At least two frequencies in a rank-2 array expected.')
    weighted_average = np.average(freq, axis=0, weights=weights)
    H_avg_freq = shannon_entropy(weighted_average, unit)
    H_freq = shannon_entropy(freq, unit)
    avg_H_freq = np.average(H_freq, weights=weights)
    JSD = H_avg_freq - avg_H_freq
    return JSD

