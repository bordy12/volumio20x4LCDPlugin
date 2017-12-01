from os import *
from time import *
from sys import *

def sendToLCD(lineNum, textToDisplay): #This function will send a string to the LCD screen
	#TODO: Unicode support/disregard. If unicode chars are found, what to do? Dont send the string? Try to send them anyway? Send '????????????'?
	#emulating LCD using terminal-window at the moment
	print(str(lineNum) + ': ' + str(textToDisplay))
try:
	# Allow people to ask for help using -h, help or --help
	if(argv[1] == "--help" or argv[1] == "help" or argv[1] == "-h"):
		print("Usage: python scrolltext.py '<line one text>' '<line two text>' '<line three text>' '<line four text>'\nDon't forget the quotes")
		exit(0)  # Quit after showing the help-text

	#TODO: change these in future so they get actual music info from mdp(?)-client or local webpage
	textOne = argv[1]
	textTwo = argv[2]
	textThree = argv[3]
	textFour = argv[4]
	
	restartLineOne = time()-1
	restartLineTwo = time()-1
	restartLineThree = time()-1
	restartLineFour = time()-1

	posLineOne=0
	posLineTwo=0
	posLineThree=0
	posLineFour=0

	timeWaitTimeStamp = time()
	timeWait = 0.25
	lineTimeWait = 0.75

	textLineOne =   textOne + " | " + textOne[0:20]
	textLineTwo =   textTwo + " | " + textTwo[0:20]
	textLineThree = textThree + " | " + textThree[0:20]
	textLineFour =  textFour + " | " + textFour[0:20]
	
	writeLineOne = False
	writeLineTwo = False
	writeLineThree = False
	writeLineFour = False

	lineOneChanged = True
	lineTwoChanged = True
	lineThreeChanged = True
	lineFourChanged = True
		
	lastPrintedTextLineOne = 0
	lastPrintedTextLineTwo = 0
	lastPrintedTextLineThree = 0
	lastPrintedTextLineFour = 0

	toPrintTextLineOne = 0
	toPrintTextLineTwo = 0
	toPrintTextLineThree = 0
	toPrintTextLineFour = 0

	while(True):
		if(time()-timeWaitTimeStamp >= timeWait):
		
			# Line one code starts here
			if(len(textOne) > 20):
				if(time()-restartLineOne > lineTimeWait):
					writeLineOne = True
					toPrintTextLineOne = textLineOne[posLineOne:posLineOne+20]
					lastPrintedTextLineOne = textLineOne[posLineOne:posLineOne+20]
					posLineOne = posLineOne +1
					lineOneChanged = True
					if(posLineOne >= len(textLineOne)-18):
						posLineOne = 1
						restartLineOne = time()
						lineOneChanged = False
					timeStampLineOne = time()
			else:
				toPrintTextLineOne = textOne
				writeLineOne = True
			
			# Line two code starts here
			if(len(textTwo) > 20):
				if(time()-restartLineTwo > lineTimeWait):
					writeLineTwo = True
					toPrintTextLineTwo = textLineTwo[posLineTwo:posLineTwo+20]
					lastPrintedTextLineTwo = textLineTwo[posLineTwo:posLineTwo+20]
					posLineTwo = posLineTwo +1
					lineTwoChanged = True
					if(posLineTwo >= len(textLineTwo)-18):
						posLineTwo = 1
						restartLineTwo = time()
						lineTwoChanged = False
					timeStampLineTwo = time()
			else:
				toPrintTextLineTwo = textTwo
				writeLineTwo = True
				
			# Line three code starts here
			if(len(textThree) > 20):
				if(time()-restartLineThree > lineTimeWait):
					writeLineThree = True
					toPrintTextLineThree = textLineThree[posLineThree:posLineThree+20]
					lastPrintedTextLineThree = textLineThree[posLineThree:posLineThree+20]
					posLineThree = posLineThree +1
					lineThreeChanged = True
					if(posLineThree >= len(textLineThree)-18):
						posLineThree = 1
						restartLineThree = time()
						lineThreeChanged = False
					timeStampLineThree = time()
			else:
				toPrintTextLineThree = textThree
				writeLineThree = True
				
			# Line four code starts here
			if(len(textFour) > 20):
				if(time()-restartLineFour > lineTimeWait):
					writeLineFour = True
					toPrintTextLineFour = textLineFour[posLineFour:posLineFour+20]
					lastPrintedTextLineFour = textLineFour[posLineFour:posLineFour+20]
					posLineFour = posLineFour +1
					lineFourChanged = True
					if(posLineFour >= len(textLineFour)-18):
						posLineFour = 1
						restartLineFour = time()
						lineFourChanged = False
					timeStampLineFour = time()
			else:
				toPrintTextLineFour = textFour
				writeLineFour = True
			
			if(lineOneChanged == True and writeLineOne == True):
				sendToLCD(0, toPrintTextLineOne)
				writeLineOne = False
				lineOneChanged = False
			if(lineTwoChanged == True and writeLineTwo == True):
				sendToLCD(1, toPrintTextLineTwo)
				writeLineTwo = False
				lineTwoChanged = False
			if(lineThreeChanged == True and writeLineThree == True):
				sendToLCD(2, toPrintTextLineThree)
				writeLineThree = False
				lineThreeChanged = False
			if(lineFourChanged == True and writeLineFour == True):
				sendToLCD(3, toPrintTextLineFour)
				writeLineFour = False
				lineFourChanged = False

			timeWaitTimeStamp = time()

except IndexError:
	print("Not enough arguments were given (I need 4 arguments)\nExiting...")
	exit(0)

