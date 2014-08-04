# events-example1-no-globals.py
# Demos timer, mouse, and keyboard events

# Search for "DK" in comments for all the changes
# required to eliminate globals.

from Tkinter import *
import math
import time
import string
import datetime
import tkFileDialog
from numpy import arange,array,ones#,random,linalg
from pylab import plot,show
from scipy import stats
import matplotlib.pylab as plt
import os.path


def mousePressed(canvas, event):
    data=canvas.data
    if data.start:
#        print data.clicks
        
        if (canvas.data.errorMade==0): #if first time clicking at a circle,
            canvas.data.listX.append(event.x)
            canvas.data.listY.append(event.y)

        if ( ((event.x-data.centerX)**2)+((event.y-data.centerY)**2)<\
                ((data.circleWidth/2)**2) ):
            canvas.data.listcX.append(canvas.data.centerX)
            canvas.data.listcY.append(canvas.data.centerY)

            if (not canvas.data.errorMade): #make it so that it only checks the first error. ie multiple errors don't matter
                canvas.data.errorMargin.append(0)
            canvas.data.errorClicks=[]
            canvas.data.errorMade=0
            
            canvas.data.clicks+=1
            recordTime(canvas)
            resetPath(canvas)
        else: #clicked outside of the circle
            errorX=event.x-canvas.data.centerX
            errorY=event.y-canvas.data.centerY
            value=(errorX**2)+(errorY**2)
            errorDel= math.sqrt(value)-(canvas.data.circleWidth/2)
            if (not canvas.data.errorMade): #make it so that it only checks the first error. ie multiple errors don't matter
                canvas.data.error.append(canvas.data.clicks)
                canvas.data.errorMargin.append(errorDel)
                print canvas.data.errorMargin
                canvas.data.errorClicks.append([event.x,event.y])
                canvas.data.errorMade=1

    else: #so this is for the start screen, when choosing devices
        mouseButtonPressed(canvas,event)
    redrawAll(canvas)

def mouseButtonPressed(canvas,event):
    x1=550
    y1=50
    x2=580
    y2=80
    #mouse
    if (x1<=event.x<=x2 and y1<=event.y<=y2):
        canvas.data.circleMouse="green"
        canvas.data.trackpad=None 
        canvas.data.fingers=None
        canvas.data.secondTime=None
    if (x1<=event.x<=x2 and y1+50<=event.y<=y2+50):
        canvas.data.circleMouse=None
        canvas.data.trackpad="green" 
        canvas.data.fingers=None
        canvas.data.secondTime=None
    if (x1<=event.x<=x2 and y1+100<=event.y<=y2+100):
        canvas.data.circleMouse=None
        canvas.data.trackpad=None 
        canvas.data.fingers="green"
        canvas.data.secondTime=None
    if (x1<=event.x<=x2 and y1+150<=event.y<=y2+150):
        canvas.data.circleMouse=None
        canvas.data.trackpad=None
        canvas.data.fingers=None
        canvas.data.secondTime="green"

def recordTime(canvas):
    elapsed=time.time()-canvas.data.time
    canvas.data.times.append(elapsed)    

def resetPath(canvas):
    canvas.data.trajectories.append(canvas.data.path)
    canvas.data.allPathTimes.append(canvas.data.pathTimes)
    canvas.data.path=[]
    canvas.data.pathTimes=[]
#    print canvas.data.trajectories

def motion(canvas, event): #store in a list and then delete lk hlaf
    if canvas.data.start: 
        x, y = event.x, event.y
        canvas.data.path.append((x,y))
        elapsed=time.time()-canvas.data.time
        canvas.data.pathTimes.append(elapsed)


def keyPressed(canvas, event):
    if (canvas.data.start==False and canvas.data.nameSet==True and event.keysym=="space"):
        canvas.data.start=True
        canvas.data.startScreen=False

        #set canvas.data.device
        setDeviceName(canvas)

        startClock(canvas)
        canvas.create_text(canvas.data.width/2, canvas.data.height/2, text=str(time.time()-canvas.data.time), font="Times 30")
    elif (canvas.data.start==False and canvas.data.nameSet==False):
        if event.keysym in string.ascii_letters:
            canvas.data.name=canvas.data.name+event.keysym
        elif event.keysym in string.digits:
            canvas.data.name=canvas.data.name+event.keysym
        elif event.keysym=="space":
            canvas.data.name=canvas.data.name+" "
        elif event.keysym=="BackSpace":
            canvas.data.name=canvas.data.name[:-1]
#            print canvas.data.name
        elif event.keysym=="Return":
            canvas.data.nameSet=True
    elif (canvas.data.start==True):
        canvas.data.keyPressed.append(canvas.data.clicks)
#        print (canvas.data.clicks, event.keysym) #see if a key was pressed
    redrawAll(canvas)


def setDeviceName(canvas):
    if canvas.data.circleMouse:
        canvas.data.device="mouse"
    elif canvas.data.trackpad:
        canvas.data.device="trackpad"
    elif canvas.data.fingers:
        canvas.data.device="fingers"
    else:
        canvas.data.device="2ndTime"

def startClock(canvas):
    canvas.data.time=time.time()




def timerFired(canvas):
    redrawAll(canvas)
    canvas.data.timerCounter += 1
    delay = 250 # milliseconds
    def f():
        timerFired(canvas) # DK: define local fn in closure
    canvas.after(delay, f) # pause, then call timerFired again


def redrawAll(canvas):   # DK: redrawAll() --> redrawAll(canvas)
    canvas.delete(ALL)
    if canvas.data.startScreen: #draw start screen
        drawStartScreen(canvas)
    else: #start circles
        if (canvas.data.start): #if started
            if canvas.data.clicks<canvas.data.numberToGo:  #while there's more circles to click
                drawCircles(canvas)
                drawError(canvas)
            else: #round finished 
                canvas.data.round+=1
                canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Section Completed", font="Times 30")
                canvas.create_text(canvas.data.width/2, canvas.data.height/2+100, text="Press the spacebar to start", font="Times 30")
                sectionFinished(canvas)
        else: #when inbetween rounds (so stopped )
            if canvas.data.round<canvas.data.numberOfRounds: #inbetween
                canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Section Completed", font="Times 30")
                canvas.create_text(canvas.data.width/2, canvas.data.height/2+100, text="Press the spacebar to start", font="Times 30")
            else: #final 
                canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Testing Complete", font="Times 30")

        #otherwize doesn't do anything (So in between the experiments)

def drawStartScreen(canvas):
    if canvas.data.nameSet==False:
        if canvas.data.timerCounter%4<2:
            canvas.create_text(canvas.data.width/2, canvas.data.height/2-100,text="Name:"+canvas.data.name,font="Times 30")
        else:
            canvas.create_text(canvas.data.width/2, canvas.data.height/2-100,text="Name:"+canvas.data.name+"_",font="Times 30")
    else: 
        canvas.create_text(canvas.data.width/2, canvas.data.height/2-100,text="Name:"+canvas.data.name,font="Times 30")

    canvas.create_text(canvas.data.width/2, canvas.data.height/2, text="Instructions:\n First, enter your name. Press enter when completed. \n Click the green circle", font="Times 30")
    canvas.create_text(canvas.data.width/2, canvas.data.height/2+100, text="Press the spacebar to start", font="Times 30")

    x1=550
    y1=50
    x2=580
    y2=80
    canvas.create_rectangle(x1,y1,x2,y2, fill=canvas.data.circleMouse) #mouse    
    canvas.create_text(x2+5, y1+15, text="Mouse", font="Times 14", anchor="w")
    canvas.create_rectangle(x1,y1+50,x2,y2+50, fill=canvas.data.trackpad) #trackpad 
    canvas.create_text(x2+5, y1+65, text="Trackpad", font="Times 14", anchor="w")
    canvas.create_rectangle(x1,y1+100,x2,y2+100, fill=canvas.data.fingers) #fingers
    canvas.create_text(x2+5, y1+115, text="Fingers", font="Times 14", anchor="w")
    canvas.create_rectangle(x1,y1+150,x2,y2+150, fill=canvas.data.secondTime) #2nd time
    canvas.create_text(x2+5, y1+165, text="2nd Time", font="Times 14", anchor="w")


#create options for which device the user is using

def drawCircles(canvas):
    angle=(math.pi/2)-math.pi*(canvas.data.clicks)/25

    cX=(canvas.data.width/2)+(canvas.data.diameter/2)*math.cos(angle)*((-1)**canvas.data.clicks)
    cY=(canvas.data.height/2)-(canvas.data.diameter/2)*math.sin(angle)*((-1)**canvas.data.clicks)
    canvas.data.centerX=cX
    canvas.data.centerY=cY

    x1=cX-canvas.data.circleWidth/2
    y1=cY-canvas.data.circleWidth/2
    x2=cX+canvas.data.circleWidth/2
    y2=cY+canvas.data.circleWidth/2
    canvas.create_oval(x1,y1,x2,y2, fill="green")

def drawError(canvas):
    for i in xrange(len(canvas.data.errorClicks)):
        cX=canvas.data.errorClicks[i][0]
        cY=canvas.data.errorClicks[i][1]
        x1=cX-2
        y1=cY-2
        x2=cX+2
        y2=cY+2
        canvas.create_oval(x1,y1,x2,y2, fill="red")

def sectionFinished(canvas):
    if (canvas.data.round==1):
        writeName(canvas)
        createDirectory(canvas)
    writeFiles(canvas)
    writeGraphFiles(canvas)
    writeTracking(canvas)
    readFile(canvas)
    setSecondaryValues(canvas)

def createDirectory(canvas):
    path="./userData/"
    savedTitle=canvas.data.name
    i=0
    value=True
    while value:
        if (i==0):
            if not os.path.exists(path+savedTitle):
                os.makedirs(path+savedTitle)
                value=False
            else:
                i+=1
        else:
            if not os.path.exists(path+savedTitle+str(i)):
                os.makedirs(path+savedTitle+str(i))
                value=False
            else:
                i+=1
    if i==0:
        canvas.data.directoryPath=path+savedTitle+"/"
        canvas.data.directoryPath=canvas.data.directoryPath.rstrip('\n')

    else:
        canvas.data.directoryPath=path+savedTitle+str(i)+"/"
        canvas.data.directoryPath=canvas.data.directoryPath.rstrip('\n')


def writeName(canvas):
    path="./userData/"
    savedTitle="userName"
    f=open(savedTitle, 'w')
    f.write(canvas.data.name)
    f.close()

def writeFiles(canvas):
    path=canvas.data.directoryPath
    savedTitle=path+str(canvas.data.name)+str(canvas.data.device)+str(canvas.data.configuration)+".dat"

    f=open(savedTitle, 'w')
#Find a way to organize data
    date = str(datetime.date.today())
    f.write(canvas.data.name+","+str(canvas.data.configuration).strip()+","+date+"\n\n")
        #Header: subject name, configuration file used, date, 
    f.write("Target#, time, targetX, targetY, clicked, keyPressed, width, distance, errorMargin\n")
        #write Body Header 
    for x in xrange(canvas.data.numberToGo):
        clicked=checkClicked(x, canvas)
        key=checkKeyPressed(x,canvas)
        stuff= str(x)+","+str(canvas.data.times[x])+","+\
            str(canvas.data.listcX[x])+","+str(canvas.data.listcY[x])+","+\
            str(canvas.data.listX[x])+","+str(canvas.data.listY[x])+","+\
            clicked+","+key+","+str(canvas.data.circleWidth)+","+\
            str(canvas.data.diameter)+","+str(canvas.data.errorMargin[x])+"\n"
        f.write(stuff)
        #Write body information
    f.close()


def writeGraphFiles(canvas):
    path=canvas.data.directoryPath
    savedTitle=path+str(canvas.data.name)+str(canvas.data.device)+str(canvas.data.configuration)+str('graph')+".grp"

    f=open(savedTitle, 'w')
    date = str(datetime.date.today())
    f.write(canvas.data.name+","+str(canvas.data.configuration)+","+date+"\n\n")
    for x in xrange(canvas.data.numberToGo):
        clicked=checkClicked(x, canvas)
        if x==0:
            stuff=str(canvas.data.times[x])+","+str(clicked)+"\n"
        else:
            stuff=str(canvas.data.times[x]-canvas.data.times[x-1])+","+str(clicked)+"\n"
        f.write(stuff)
    f.write(str(doAnalysis(canvas)[0])+"\n")
    f.write(str(doAnalysis(canvas)[1])+"\n")
    f.close()


def checkClicked(x,canvas):
    for i in xrange(len(canvas.data.error)):
        if canvas.data.error[i]==x:
            return "1"
    return "0"

def checkKeyPressed(x, canvas):
    for i in xrange(len(canvas.data.keyPressed)):
        if canvas.data.keyPressed[i]==x:
            return "1"
    return "0"

def writeTracking(canvas):
    path=canvas.data.directoryPath
    savedTitle=path+str(canvas.data.name)+str(canvas.data.device)+str(canvas.data.configuration)+str('tracking')+".trk"

    f=open(savedTitle, 'w')
    date = str(datetime.date.today())
    f.write(canvas.data.name+","+str(canvas.data.configuration)+","+date+"\n")
    f.write("Target#, times, x, y \n")
    for x in xrange(canvas.data.numberToGo): #this x is wrt to clicks
        stuff=""
        timesForThisRound=canvas.data.allPathTimes[x] #1d list of [time1, time2, time3....]
        trajectory=canvas.data.trajectories[x] #1d list of (x,y)
#        print trajectory
#        print x
        for i in xrange(len(trajectory)):
            stuff=str(timesForThisRound[i]) #time 
            stuff=stuff+","+str(trajectory[i][0]) #x coordinate
            stuff=stuff+","+str(trajectory[i][1]) #y coordinate
            thing=str(x)+", "+str(stuff)+"\n"
            f.write(thing)
    f.close()

def openFile(canvas):
    root = Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
    canvas.data.condition=file_path
    #Set diameter and width to condition
    readFile(canvas)

def readFile(canvas):
    with open(canvas.data.condition) as f:
        for x in xrange(canvas.data.round+1):
            canvas.data.configuration=str(f.readline())
            if canvas.data.configuration=="":
                break
            f.readline()
            canvas.data.circleWidth=int(f.readline())
            f.readline()
            canvas.data.diameter=int(f.readline())

#this is at the end of each to analysize
def doAnalysis(canvas):
    xi = arange(0,26)
    A = array([ xi, ones(26)])
    # linearly generated sequence
    y = canvas.data.times
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
    return stats.linregress(xi,y)

def init(canvas):

    canvas.data.diameter=30 #Filler in case of error
    canvas.data.circleWidth=10 #filler 

    canvas.data.round=0
    canvas.data.numberOfRounds=3


#################################################################################
#condition
    openFile(canvas)
#################################################################################
#set values
    setInitialValues(canvas) #doesn't change throughotu
    setSecondaryValues(canvas) #changes per round


def setInitialValues(canvas):
    canvas.data.name=""
    canvas.data.nameSet=False
    canvas.data.startScreen=True #Set to draw the starting screen
    canvas.data.device=""
    canvas.data.circleMouse=None
    canvas.data.trackpad=None 
    canvas.data.fingers=None
    canvas.data.secondTime=None

    canvas.data.directoryPath=""

def setSecondaryValues(canvas): #for setting values 
##########################################################################################################
    canvas.data.times=[] #array of all the times it took to press the circle
    canvas.data.trajectories=[] #2d array of all paths
    canvas.data.path=[]  #1d array of a single path.
    canvas.data.pathTimes=[] 
    canvas.data.allPathTimes=[]
##############################################################################################################
    canvas.data.error=[]
    canvas.data.errorMargin=[]
    canvas.data.errorClicks=[]
    canvas.data.errorMade=0 
    canvas.data.keyPressed=[]
    canvas.data.listcX=[] #list of the location of the circle coordintes
    canvas.data.listcY=[]

    canvas.data.listX=[]#list of where user clicked X axis
    canvas.data.listY=[] #list of where user clicked Y axis


 #########################################################################################################
    canvas.data.timerCounter = 0
 #########################################################################################################
    canvas.data.numberToGo=26 #number of clicks to do
    canvas.data.clicks=0
#########################################################################################################
    canvas.data.start=False #set not to start. Once enter is pressed starts.


def run():
    # create the root and the canvas
    root = Tk()
    cHeight=700
    cWidth=700
    canvas = Canvas(root, width=cWidth, height=cHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=cWidth
    canvas.data.height=cHeight
    init(canvas) 
    root.bind("<Button-1>", lambda event:mousePressed(canvas,event))
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    root.bind("<Motion>", lambda event: motion(canvas, event))
    timerFired(canvas) 
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
run()



########### copy-paste below here ###########

#https://docs.python.org/2/tutorial/inputoutput.html
#http://stackoverflow.com/questions/6159900/correct-way-to-write-line-to-file-in-python
#http://www.mth.msu.edu/~jhall/classes/mth880-05/projects/latin.pdf #Latin Method



