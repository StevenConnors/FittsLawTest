
#canvas.data.times is not working properly

#canvas.data.homingTime and homingTimes is for the time it takes for the user to move mouse, hom1

from Tkinter import *
import math
import time
import string
import datetime
import tkFileDialog
import os.path
import random

def mousePressed(canvas, event):
<<<<<<< HEAD
	if canvas.data.start:
		if (canvas.data.pressButtons==False): #if first time clicking at a circle,

			#on the first click, record the location
			if canvas.data.errorMade==0:
				canvas.data.listX.append(event.x)
				canvas.data.listY.append(event.y)
				canvas.data.listcX.append(canvas.data.centerX)
				canvas.data.listcY.append(canvas.data.centerY)
			#If correct click, 
			if ( ((event.x-canvas.data.centerX)**2)+((event.y-canvas.data.centerY)**2)<((canvas.data.circleWidth/2)**2) ):

				if (not canvas.data.errorMade): #make it so that it only checks the first error. ie multiple errors don't matter
					canvas.data.errorMargin.append(0)
				canvas.data.errorClicks=[]
				canvas.data.errorMade=0
				canvas.data.clicks+=1
	#Eedit: after a successful click, raise a flg forcing to type the keyboard
				canvas.data.pressButtons=True
				canvas.data.firstTime=True
	#this time.time is to ignore the time to press keys:
				canvas.data.buttonTime=time.time()

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
					canvas.data.errorClicks.append([event.x,event.y])
					canvas.data.errorMade=1
	else: #so this is for the start screen, when choosing devices
		mouseButtonPressed(canvas,event)
	redrawAll(canvas)
=======
    data=canvas.data
    if data.start:
#        print data.clicks

        if (canvas.data.errorMade==0 and canvas.data.pressButtons==False): #if first time clicking at a circle,
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
#Eedit: after a successful click, raise a flg forcing a button press
            canvas.data.pressButtons=True
#this time.time is to ignore the time to press keys:
            canvas.data.buttonTime=time.time()

        else: #clicked outside of the circle
            errorX=event.x-canvas.data.centerX
            errorY=event.y-canvas.data.centerY
            value=(errorX**2)+(errorY**2)
            errorDel= math.sqrt(value)-(canvas.data.circleWidth/2)
            if (not canvas.data.errorMade): #make it so that it only checks the first error. ie multiple errors don't matter
                canvas.data.error.append(canvas.data.clicks)
                canvas.data.errorMargin.append(errorDel)
                canvas.data.errorClicks.append([event.x,event.y])
                canvas.data.errorMade=1
    else: #so this is for the start screen, when choosing devices
        mouseButtonPressed(canvas,event)
    redrawAll(canvas)
>>>>>>> FETCH_HEAD

def mouseButtonPressed(canvas,event):
	x1=550
	y1=50
	x2=580
	y2=80
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
	#if canvas.data.buttonTime==0:
	#    elapsed=time.time()-canvas.data.time
	#else:
	#    elapsed=(time.time()-canvas.data.time)-(time.time()-canvas.data.buttonTime)
	elapsed=(time.time()-canvas.data.time)
	canvas.data.times.append(elapsed)   

def resetPath(canvas):
	canvas.data.trajectories.append(canvas.data.path)
	canvas.data.allPathTimes.append(canvas.data.pathTimes)
	canvas.data.path=[]
	canvas.data.pathTimes=[]
#    print canvas.data.trajectories
#Determine which word to type
	canvas.data.random = random.randint(0,49)

def motion(canvas, event): #store in a list and then delete lk hlaf
	if canvas.data.start: 
		x, y = event.x, event.y
		canvas.data.path.append((x,y))
		elapsed=time.time()-canvas.data.time
		canvas.data.pathTimes.append(elapsed)
		if canvas.data.homingTime!=0:
			canvas.data.homingTimes.append(time.time()-canvas.data.homingTime)
			canvas.data.homingTime=0

def startClock(canvas):
	canvas.data.time=time.time()
	canvas.data.homingTime=time.time()


def keyPressed(canvas, event):
	#While actual testing.
	if (canvas.data.start==False and canvas.data.nameSet==True and event.keysym=="space"):
		canvas.data.start=True
		canvas.data.startScreen=False
		#set canvas.data.device
		setDeviceName(canvas)
		startClock(canvas)
	elif (canvas.data.start and canvas.data.pressButtons):
#This is for typing
		#Gets the homing time for typing
		if canvas.data.firstTime:
			canvas.data.firstTime=False
			canvas.data.buttonTimes.append(time.time()-canvas.data.buttonTime)
			canvas.data.buttonTime=0
			canvas.data.typingTime=time.time()
		if event.keysym in string.ascii_letters:
			canvas.data.typed = "".join((canvas.data.typed, event.keysym))
		elif event.keysym=="BackSpace":
			canvas.data.typed=canvas.data.typed[:-1]

		#check if correct word
		if canvas.data.typed == canvas.data.currentWord:
			canvas.data.pressButtons=False
			canvas.data.typingTimes.append(time.time()-canvas.data.typingTime)
			canvas.data.typingTime=0
			canvas.data.typed = ""
			canvas.data.homingTime=time.time()
			canvas.data.listOfWords.append(canvas.data.currentWord)

#Below is for set up
	elif (canvas.data.start==False and canvas.data.nameSet==False):
		if event.keysym in string.ascii_letters:
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


##########################################################################################################
######################################  Draw Things  #####################################################
##########################################################################################################

def timerFired(canvas):
	redrawAll(canvas)
	canvas.data.timerCounter += 1
	delay = 250 # milliseconds
	def f():
		timerFired(canvas) # DK: define local fn in closure
	canvas.after(delay, f) # pause, then call timerFired again

def redrawAll(canvas):   # DK: redrawAll() --> redrawAll(canvas)
	canvas.delete(ALL)

	textTime= time.time()- canvas.data.time
	textHomingOne= time.time()-canvas.data.homingTime
	textButtonTime= time.time()-canvas.data.buttonTime
	textTypingTime= time.time()-canvas.data.typingTime


	canvas.create_text(40, 20, text=("Time: %.4d "%textTime), font="Times 12")
	canvas.create_text(40, 40, text=("Time: %.4d "%textHomingOne), font="Times 12")
	canvas.create_text(40, 60, text=("Time: %.4d "%textButtonTime), font="Times 12")
	canvas.create_text(40, 80, text=("Time: %.4d "%textTypingTime), font="Times 12")

	if canvas.data.startScreen: #draw start screen
		drawStartScreen(canvas)
	else: #start circles
		if (canvas.data.start): #if started
			if canvas.data.clicks<canvas.data.numberToGo:  #while there's more circles to click
				if canvas.data.pressButtons:
					drawTyping(canvas)
				else:
					drawCircles(canvas)
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
	drawDeviceOptions(canvas)


def drawDeviceOptions(canvas):
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

def drawCircles(canvas):
	angle=(math.pi/2)-math.pi*(canvas.data.clicks)/(canvas.data.numberToGo-1)
	cX=(canvas.data.width/2)+(canvas.data.diameter/2)*math.cos(angle)*((-1)**canvas.data.clicks)
	cY=(canvas.data.height/2)-(canvas.data.diameter/2)*math.sin(angle)*((-1)**canvas.data.clicks)
	canvas.data.centerX=cX
	canvas.data.centerY=cY
	x1=cX-canvas.data.circleWidth/2
	y1=cY-canvas.data.circleWidth/2
	x2=cX+canvas.data.circleWidth/2
	y2=cY+canvas.data.circleWidth/2
	canvas.create_oval(x1,y1,x2,y2, fill="green")

def drawTyping(canvas):
	canvas.create_text(canvas.data.width/2, canvas.data.height/2-150, text="Type:"+canvas.data.typed, font="Times 40", fill="black")
	canvas.data.currentWord = canvas.data.wordList[canvas.data.random]
	canvas.create_text(canvas.data.width/2, canvas.data.height/2 - 50, text="Type:"+ canvas.data.wordList[canvas.data.random], font="Times 40", fill="black")


##########################################################################################################
######################################   I/O Things  #####################################################
##########################################################################################################

#writes the files after each section
def sectionFinished(canvas):
	if (canvas.data.round<=1):
		createDirectory(canvas)
	writeFiles(canvas)
	writeTracking(canvas)
	readFile(canvas)
	setSecondaryValues(canvas)

#creates a folder for th4e files to be saved
def createDirectory(canvas):
	path="./userDataMFLT/"
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

#Writes the .dat file which has all the data
def writeFiles(canvas):
	path=canvas.data.directoryPath
	savedTitle=path+str(canvas.data.name)+str(canvas.data.device)+str(canvas.data.configuration)+".dat"
	f=open(savedTitle, 'w')
#Find a way to organize data
	date = str(datetime.date.today())
	f.write(canvas.data.name+","+str(canvas.data.configuration).strip()+","+date+"\n\n")
		#Header: subject name, configuration file used, date, 
	f.write("Target#, time, targetX, targetY, clickX, clickY, clicked, keyPressed, width,distance, errorMargin, Homing Time1, Keyboard Homingtime, Typingtime, Word\n")
		#write Body Header 
	
	canvas.data.times= modifiedTimes(canvas)

	for x in xrange(canvas.data.numberToGo):
		clicked=checkClicked(x, canvas)
		key=checkKeyPressed(x,canvas)
		if (x<11):
			stuff = str(x) + "," + ('%.3f'%(canvas.data.times[x])) +"," + ('%.3f'%(canvas.data.listcX[x])) +"," + ('%.3f'%(canvas.data.listcY[x])) +"," +\
				('%.3f'%(canvas.data.listX[x])) +"," + ('%.3f'%(canvas.data.listY[x])) +"," + clicked +"," + \
				key +"," + str(canvas.data.circleWidth) +"," + str(canvas.data.diameter)+"," + \
				('%.3f'%(canvas.data.errorMargin[x])) +"," + ('%.3f'%(canvas.data.homingTimes[x]))+"," + \
				('%.3f'%(canvas.data.buttonTimes[x])) +"," + ('%.3f'%(canvas.data.typingTimes[x]))+ ","+str(canvas.data.listOfWords[x])+ "\n"
		else:
			stuff = str(x) + "," + ('%.3f'%(canvas.data.times[x])) +"," + ('%.3f'%(canvas.data.listcX[x])) +"," + ('%.3f'%(canvas.data.listcY[x])) +"," +\
				('%.3f'%(canvas.data.listX[x])) +"," + ('%.3f'%(canvas.data.listY[x])) +"," + clicked +"," + \
				key +"," + str(canvas.data.circleWidth) +"," + str(canvas.data.diameter)+"," + \
				('%.3f'%(canvas.data.errorMargin[x])) +"," + ('%.3f'%(canvas.data.homingTimes[x]))+ "\n"
		f.write(stuff)
		#Write body information
	f.close()

################################################################################################################################################################
def modifiedTimes(canvas):
	newTimes=[]
	for i in xrange(canvas.data.numberToGo):
		time= canvas.data.times[i]
		if (i==0):
			time = time-canvas.data.homingTimes[i]
		else:
			for j in xrange(i-1):
				time = time-canvas.data.homingTimes[j] - canvas.data.typingTimes[j-1] - canvas.data.buttonTimes[j-1]
		newTimes.append(time)

	print newTimes
	print canvas.data.times
	return newTimes
################################################################################################################################################################


#check if any errors in clicking
def checkClicked(x,canvas):
	for i in xrange(len(canvas.data.error)):
		if canvas.data.error[i]==x:
			return "1"
	return "0"

#check if any keypress errors occured
def checkKeyPressed(x, canvas):
	for i in xrange(len(canvas.data.keyPressed)):
		if canvas.data.keyPressed[i]==x:
			return "1"
	return "0"

#Writes the file which tracks mouse position
def writeTracking(canvas):
	path=canvas.data.directoryPath
	savedTitle=path+str(canvas.data.name)+str(canvas.data.device)+str(canvas.data.configuration)+"MFLTtracking"+".trk"
	f=open(savedTitle, 'w')
	date = str(datetime.date.today())
	f.write(canvas.data.name+","+str(canvas.data.configuration)+","+date+"\n")
	f.write("Target#, times, x, y \n")
	for x in xrange(canvas.data.numberToGo): #this x is wrt to clicks
		stuff=""
		timesForThisRound=canvas.data.allPathTimes[x] #1d list of [time1, time2, time3....]
		trajectory=canvas.data.trajectories[x] #1d list of (x,y)
		for i in xrange(len(trajectory)):
			stuff=str(timesForThisRound[i]) #time 
			stuff=stuff+","+str(trajectory[i][0]) #x coordinate
			stuff=stuff+","+str(trajectory[i][1]) #y coordinate
			thing=str(x)+", "+str(stuff)+"\n"
			f.write(thing)

#reads the calibration file
def openFile(canvas):
	root = Tk()
	root.withdraw()
	file_path = tkFileDialog.askopenfilename()
	canvas.data.condition=file_path
	#Set diameter and width to condition
	readFile(canvas)

#reads the calibration file
def readFile(canvas):
	with open(canvas.data.condition) as f:
		for x in xrange(canvas.data.round+1):
			canvas.data.configuration=str(f.readline()).rstrip()
			if canvas.data.configuration=="":
				break
			f.readline()
			canvas.data.circleWidth=int(f.readline())
			f.readline()
			canvas.data.diameter=int(f.readline())

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
	canvas.data.path=""


	canvas.data.wordList=[
		'candle',
		'glencoe',
		'saith',
		'chinagraph',
		'dacryon',
		'lancewood',
		'defencelessly',
		'mareograph',
		'fence',
		'weslaco',
		'tumbrel',
		'salespeople',
		'wran',
		'geophagism',
		'undercast',
		'unselfconsciousness',
		'indisputableness',
		'keifer',
		'donald',
		'sicilies',
		'counteraction',
		'warmthless',
		'leaky',
		'groveling',
		'shinnston',
		'korah',
		'understage',
		'phycocolloid',
		'autopotamic',
		'israel',
		'floweriness',
		'cephalothorax',
		'disincline',
		'involutional',
		'approvability',
		'illegitimatizing',
		'unfired',
		'quadrivalency',
		'nonsawing',
		'blackwood',
		'fountainless',
		'marlene',
		'lapstreak',
		'republicanising',
		'iwis',
		'mihail',
		'overfemininity',
		'cannily',
		'nonutterance',
		'doorstep']

def setSecondaryValues(canvas): #for setting values that are reset after every round

	canvas.data.time=0
	canvas.data.times=[] #array of all the times it took to press the circle
	canvas.data.trajectories=[] #2d array of all paths
	canvas.data.path=[]  #1d array of a single path.
	canvas.data.pathTimes=[] 
	canvas.data.allPathTimes=[]

	canvas.data.error=[]
	canvas.data.errorMargin=[]
	canvas.data.errorClicks=[]
	canvas.data.errorMade=0 
	canvas.data.keyPressed=[]
	canvas.data.listcX=[] #list of X coord of the circle center
	canvas.data.listcY=[] #list of Y coord of the circle center

	canvas.data.listX=[]#list of where user clicked X coord
	canvas.data.listY=[] #list of where user clicked Y coord

	canvas.data.timerCounter = 0
 
	canvas.data.numberToGo=12 #number of clicks to do
	canvas.data.clicks=0 #how many I've successfully clicked

	canvas.data.start=False #set not to start. Once name is entered the program starts.

	canvas.data.typed=""
	canvas.data.currentWord=""
	canvas.data.pressButtons=False
 
 	canvas.data.homingTime=0
	canvas.data.homingTimes=[]

	canvas.data.buttonTime=0
	canvas.data.buttonTimes=[]

	canvas.data.typingTime=0
	canvas.data.typingTimes=[]

	canvas.data.listOfWords=[]
	canvas.data.firstTime=False

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


""""

canvas.data.wordList=[
		'candle',
		'glencoe',
		'saith',
		'chinagraph',
		'dacryon',
		'lancewood',
		'defencelessly',
		'mareograph',
		'fence',
		'weslaco',
		'tumbrel',
		'salespeople',
		'wran',
		'geophagism',
		'undercast',
		'unselfconsciousness',
		'indisputableness',
		'keifer',
		'donald',
		'sicilies',
		'counteraction',
		'warmthless',
		'leaky',
		'groveling',
		'shinnston',
		'korah',
		'understage',
		'phycocolloid',
		'autopotamic',
		'israel',
		'floweriness',
		'cephalothorax',
		'disincline',
		'involutional',
		'approvability',
		'illegitimatizing',
		'unfired',
		'quadrivalency',
		'nonsawing',
		'blackwood',
		'fountainless',
		'marlene',
		'lapstreak',
		'republicanising',
		'iwis',
		'mihail',
		'overfemininity',
		'cannily',
		'nonutterance',
		'doorstep']
		"""
