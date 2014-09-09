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

userNum = 32
deviceNum = 6
testNum = 4
for i in range(userNum):
    # conds = []
    output = 'Discomfort\t'
    # Each Device
    for k in range(deviceNum):
        temp = []
        # Each Test
        for j in range(testNum):
            while True:
                seq = np.random.choice(conditions, size=3, replace=False).tolist()
                if seq not in temp:
                    break
            temp.append(seq)
            for k in seq:
                output += k
            output += '\t'
        # conds.append(temp)
        output += 'Discomfort\t'
    print output
        # print temp

    # for j in range(testNum):
    #     if j == 0:
    #         output = str(i+1)
    #     else:
    #         output = ''
    #     # Each Device
    #     for k in range(deviceNum):
    #         output += '\t{}{}{}'.format(conds[k][j][0], conds[k][j][1], conds[k][j][2])
    #     print output
    # print ''
