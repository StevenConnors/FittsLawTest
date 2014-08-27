'''Generate random sequence'''
import random

seq = ['FA', 'M', 'FR', 'T']
order = [[0, 1, 2, 3], [1, 2, 3, 0], [3, 0, 1, 2], [2, 3, 0, 1]]

cond = ['A', 'B', 'C']
orderC = [0, 1, 2]

for i in range(30):
    random.shuffle(order)
    output0 = [seq[x] for x in order[0]]
    output1 = [seq[x] for x in order[1]]
    print '{}\t\t{}\t\t{}\t\t{}\t\t\t{}\t\t{}\t\t{}\t\t{}'.format(output0[0], output0[1], output0[2], output0[3], \
        output1[0], output1[1], output1[2], output1[3])

for i in range(30):
    # Each Test
    for j in range(4):
        if j == 0:
            output = str(i+1)
        else:
            output = ''
        # Each Device
        for k in range(10):
            random.shuffle(orderC)
            output += '\t{}{}{}'.format(cond[orderC[0]], cond[orderC[1]], cond[orderC[2]])
        print output
    print ''
