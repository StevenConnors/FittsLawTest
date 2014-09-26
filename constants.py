def firstInit(canvas):
	canvas.data.diameter=30 #Filler in case of error
	canvas.data.circleWidth=10 #filler 
	canvas.data.round=0
	canvas.data.numberOfRounds=3
	canvas.data.finished=False
#condition
	openFile(canvas)
#set values
	setInitialValues(canvas) #doesn't change throughotu
	setSecondaryValues(canvas) #changes per round
	canvas.data.random = random.randint(0,len(canvas.data.wordList)-1)#Just in case
	