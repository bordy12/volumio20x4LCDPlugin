#TODO: INSTEAD OF PRINTING DIRECTLY TO SCREEN, SET VARS AND THEN, AT THE, END SOMEWHERE, PRINT THEM! (LCD AND IT'S LIBRARY WILL LIKE THIS BETTER)

from os import *
from time import *
from sys import *

try:

	#void setup(){

	# Allow people to ask for help using -h, help or --help
	if(argv[1] == "--help" or argv[1] == "help" or argv[1] == "-h"):
		print("Usage: python scrolltext.py <text you want to scroll on line one> <line two text> <line three text> <line four text>\nDon't forget to put quotes where needed!")
		exit(0)  # Don't go ahead and scroll --help or something XD

	#plz change deez in future so they get actual music info from mdp(?)-client or local webpage
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
	lineTimeWait = 1

	textLineOne =   textOne + " | " + textOne[0:20]
	textLineTwo =   textTwo + " | " + textTwo[0:20]
	textLineThree = textThree + " | " + textThree[0:20]
	textLineFour =  textFour + " | " + textFour[0:20]

	lastPrintedTextLineOne = 0
	lastPrintedTextLineTwo = 0
	lastPrintedTextLinethree = 0
	lastPrintedTextLineFour = 0

	toPrintTextLineOne = 0
	toPrintTextLineTwo = 0
	toPrintTextLineThree = 0
	toPrintTextLineFour = 0

	#}

	#void loop(){

	while(True):
		if(time()-timeWaitTimeStamp >= timeWait):
			# Line one code starts here
			if(len(textOne) > 20):
				if(time()-restartLineOne > lineTimeWait):
					system("clear")
					toPrintTextLineOne = textLineOne[posLineOne:posLineOne+20]
					lastPrintedTextLineOne = textLineOne[posLineOne:posLineOne+20]
					posLineOne = posLineOne +1
					if(posLineOne >= len(textLineOne)-19):
						posLineOne = 0
						restartLineOne = time()
					timeStampLineOne = time()
			else:
				if(textOne != lastPrintedTextLineOne):  #We willen niet oneindig keer hetzelfde sturen naar de LCD, want dat is teveel moeite
					system("clear")
					toPrintTextLineOne = textOne
					lastPrintedTextLineOne = textOne
			# Line two code starts here
			if(len(textTwo) > 20):
				if(time()-restartLineTwo > lineTimeWait):
					system("clear")
					toPrintTextLineTwo = textLineTwo[posLineTwo:posLineTwo+20]
					lastPrintedTextLineTwo = textLineTwo[posLineTwo:posLineTwo+20]
					posLineTwo = posLineTwo +1
					if(posLineTwo >= len(textLineTwo)-19):
						posLineTwo = 0
						restartLineTwo = time()
					timeStampLineTwo = time()
			else:
				if(textTwo != lastPrintedTextLineTwo):  #We willen niet oneindig keer hetzelfde sturen naar de LCD, want dat is teveel moeite
					system("clear")
					toPrintTextLineTwo = textTwo
					lastPrintedTextLineTwo = textTwo
			# HIER NOG 3 ANDERE CHECKS VOOR DE OVERIGE REGELS!

			#DIT IS LELIJK DOE DIT JE SCRIPT NIET AAN STRAKS!
			if(str(toPrintTextLineOne) != str(0) or str(toPrintTextLineTwo) != str(0)):
				print(str(toPrintTextLineOne) + "\n" + str(toPrintTextLineTwo))

			timeWaitTimeStamp = time()  #MOET HELEMAAL ONDERAAN STRAKS!
	#}

except IndexError:
	print("No arguments were given (I need 4 arguments)\nExiting...")
	exit(0)
