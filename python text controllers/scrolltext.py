from os import *
from time import *
from sys import *

#plz change deez in future thank you!
textOne = argv[1]
textTwo = argv[2]
textThree = argv[3]
textFour = argv[4]

restartLineOne = time()

posLineOne=0
posLineTwo=0
posLineThree=0
posLineFour=0

timeWaitTimeStamp = time()
timeWait = 0.5

textLineOne =   textOne + " | " + textOne[0:20]
textLineTwo =   textTwo + " | " + textTwo[0:20]
textLineThree = textThree + " | " + textThree[0:20]
textLineFour =  textFour + " | " + textFour[0:20]

lastPrintedTextLineOne = 0

while(True):
	if(time()-timeWaitTimeStamp >= timeWait):
		if(len(textOne) > 20):
			if(time()-restartLineOne > 1):
				system("clear")
				print(textLineOne[posLineOne:posLineOne+20])
				lastPrintedTextLineOne = textLineOne[posLineOne:posLineOne+20]
				posLineOne = posLineOne +1
				if(posLineOne >= len(textLineOne)-19):
					posLineOne = 0
					restartLineOne = time()
				timeStampLineOne = time()
		else:
			if(textOne != lastPrintedTextLineOne):  #We willen niet oneindig keer hetzelfde sturen naar de LCD, want dat is teveel moeite
				system("clear")
				print(textOne)
				lastPrintedTextLineOne = textOne

		# HIER NOG 3 ANDERE CHECKS VOOR DE OVERIGE REGELS!

		timeWaitTimeStamp = time()  #MOET HELEMAAL ONDERAAN STRAKS!
