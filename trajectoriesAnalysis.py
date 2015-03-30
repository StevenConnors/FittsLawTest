import matplotlib.pylab as plt
import Tkinter, Tkconstants, tkFileDialog
import numpy as np
import dataReader as dR

def rotation(angle,x,y):
    #Find a way to keep this matrix in memory
    rotMat=[[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]
    rotMat=np.matrix(rotMat)
    mat=np.matrix([x,y])
    
    print(rotMat)
    print(mat)
    
    output=np.inner(rotMat,mat.T)
    print(output)
    return output.T

def lineAngle(x,y):
    '''
    Calculates the angle of line with respect to the horizontal in a 2D plane
    it needs two points x,y where
    x=[x1,x2]
    y=[y1,y2]
    and (x1,y1) is the starting point
    and (x2,y2) is the ending point
    '''
    x1=x[0]
    x2=x[1]
    y1=y[0]
    y2=y[1]
    
    dx=np.abs(x1-x2)
    dy=np.abs(y1-y2)
    
    ang=np.arctan(dy/dx)
    
    if x1<x2 and y1>y2:
        return ang
    if x1<x2 and y1<y2:
        return -ang
    if x1>x2 and y1>y2:
        return ang+180
    if x1>x2 and y2>y1:
        return 180-ang
    
    

# filename=tkFileDialog.askopenfilename()
# print(filename)
# filename='/Users/julian/git/FittsLawTest/userDataMFLT/a_vs_t_extra/test/testfingersAMFLTtracking.trk'
filename='/Users/julian/git/FittsLawTest/userDataMFLT/relative_vs_absolute/p1/absolute/p1a1/p1a1fingersAMFLTtracking.trk'

temp=dR.csvReader(filename, delimiter=',', headerLines=2)
header=temp['header'][1]
data=temp['data']
x=[]
y=[]
indexs=[]
target=[]
labels=[]
times=[]

for i in range(len(data)):
    target.append(int(data[i][0]))
    times.append(float(data[i][1]))
    x.append(int(data[i][2]))
    y.append(int(data[i][3]))
    labels.append(data[i][4])
    if 'Display' in data[i][-1]:
        indexs.append(i) 
        
        

print('done')


##Getting the data segments

segments={'start':[],'end':[]}
angles=[]
for i in range(len(indexs)):
    if i>0:
        start=indexs[i-1]
        end=indexs[i]
        segments['start'].append(start)
        segments['end'].append(end)
        xs=[x[start],x[end]]
        ys=[y[start],y[end]]
        angles.append(lineAngle(xs,ys))
        



for i in range(len(indexs)-1):
    start=segments['start'][i]
    end=segments['end'][i]
    plt.plot(x[start:end+1],y[start:end+1],'x-')

plt.show()

# x=[0,1]
# y=[0,0]

# x=xs
# y=xs
data=rotation(np.pi/3,x,y)
plt.plot(x,y,'xr')
xr=data[:,0]
yr=data[:,1]
plt.plot(xr,yr,'xb')
plt.show()

#Next step :
# Compute the line that connects the start and end points
# once you do that find the angle of that line with respect to the horizontal
# putting always the beginning on the left and the end on the right
# this can be done using the matrix rotation algorithm
# similarly translate the matrix so that it always goes from zero to 400 which I believe is the lenght
# Once this transformation is done the area under the curve can be calculated analyzed as well
# things like the overshot can be calculated as well
# The integral of this curve is actually the total distance since I do have the target number this information can
# be incorporated into the database
