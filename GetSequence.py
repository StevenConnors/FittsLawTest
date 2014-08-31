'''Generate random sequence'''
import random
import numpy as np

seq = ['FA', 'M', 'FR', 'T']
order = [[0, 1, 2, 3], [1, 2, 3, 0], [3, 0, 1, 2], [2, 3, 0, 1]]

for i in range(30):
    random.shuffle(order)
    output0 = [seq[x] for x in order[0]]
    output1 = [seq[x] for x in order[1]]
    print '{}\t\t{}\t\t{}\t\t{}\t\t\t{}\t\t{}\t\t{}\t\t{}'.format(output0[0], output0[1], output0[2], output0[3], \
        output1[0], output1[1], output1[2], output1[3])

conditions = ['A','B','C']

for i in range(30):
    conds = []
    # Each Device
    for k in range(10):
        temp = []
        # Each Test
        for j in range(4):
            while True:
                seq = np.random.choice(conditions, size=3, replace=False).tolist()
                if seq not in temp:
                    break
            temp.append(seq)
        conds.append(temp)
    for j in range(4):
        if j == 0:
            output = str(i+1)
        else:
            output = ''
        # Each Device
        for k in range(10):
            output += '\t{}{}{}'.format(conds[k][j][0], conds[k][j][1], conds[k][j][2])
        print output
    print ''
