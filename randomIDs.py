

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
print(conds)