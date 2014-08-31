

import numpy as np


#number of participants
numPart=30 
conditions=['A','B','C']
conds=[]


for i in range(30):
    temp=[]
    for i2 in range(4):
        while True:
            seq=np.random.choice(conditions,size=3,replace=False).tolist()
            if seq not in temp:
                break
        temp.append(seq)
    conds.append(temp)
for i in conds:
    for i2 in i:
        print('%s\t%s\t%s'%(i2[0],i2[1],i2[2]))