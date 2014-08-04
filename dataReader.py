
#===============================================================================
# The functions in this file read data from files in different formats
#
# Copyright (C) Julian Ramos 2014
#===============================================================================

import dataSearchUtils as dSu

def csvReader(filename,delimiter='\t',headerLines=3):
    '''
    This function reads csv files that contain a header
    the header is simply specified as the first lines in the file
    '''
    header=[]
    data=[]
    lineNum=0
    temp=[]
    
    with open(filename,'r') as file:
        
        
        for line in file:
            temp.append(line.strip().split(delimiter))
            
    for key,row in enumerate(temp):
        if key<headerLines:
            header.append(row)
        else:
            data.append(row)
    return {'data':data,'header':header}
                

if __name__=='__main__':
    filename='F:/Activity_RS/Last data set/FeatureDataset/S01_1.dat'            
    data=csvReader(filename)
    print(data['header'])
    print(data['data'][0])



        
