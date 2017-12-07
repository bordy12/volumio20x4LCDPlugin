#! /usr/bin/env python
from os import *
from time import *
from sys import *

from mpd import MPDClient

mpd_host = "127.0.0.1"
mpd_port = "6600"
mpd_password = "volumio"

client = MPDClient()
client.connect(mpd_host, mpd_port)

#import lcd-related python libs
from lcd_display import lcd

#make sure python knows what an lcd is
my_lcd = lcd()

#make lcd-positions just work properly
lcd_position=[1,3,2,4]

#define some options
moveText = 1 #For stability, This should be remain 1. This script can handle >= 2 though, but it will look a bit weird as it is right now.
infoRefreshTimeWait = 0.2
timeWaitTimeStamp = 0
infoRefreshTimeStamp = time()
timeWait = 1 # Amount of time to wait before moving a piece of text on the lcd
lineTimeWait = 0  # Set to 0, unless the moving text should wait extra long before scrolling

#making sure it doesn't throw errors
songInfo=[' ', ' ', ' ',' ']
textOne = ' '
textTwo = ' '
textThree = ' '
textFour = ' '

def sendToLCD(lineNum, textToDisplay): #This function will send a string to the LCD screen
	print('Send to LCD line ' + str(lineNum) + ': ' + str(textToDisplay))
        #TODO: Unicode support/disregard. If unicode chars are found, what to do? Dont send the string? Try to send them anyway? Send '????????????'?
        my_lcd.display_string(textToDisplay, lcd_position[lineNum])
        #print(str(lineNum) + ': ' + str(textToDisplay)) #DEBUG!

def updateLCDinfo():
	returnData = [' ', ' ', ' ', ' ']
	currentSong = client.currentsong()
	if 'title' in currentSong: #This line avoids KeyErrors. It checks if the dict currentSong has some useful info. If no info is found, it will say 'Stopped' on the lcd-screen
		if(str(currentSong) != '{}'):
			if 'http' in currentSong['file']: #Check for any webstreams before returning information
				#It's a radio-stream from the interwebs! Peform some magic on the title, because it also contains the artist's name
				title = currentSong['title']
				if '-' in title or ':' in title:
					titleSplit = title.replace(':', '-').split('-')
					title = titleSplit[0]
					artist = titleSplit[1]
					if(artist[0:1] == ' '):  # split() does it's job correctly, but I don't want a <space> at the beginning of informations
						artist = artist[1::]  # So info=info-first_char
					if(title[0:1] == ' '):
						title = title[1::]
								#TODO: PLZ ALSO REMOVE <space> IF IT'S THE LAST CHAR!
					print(title)
					print(artist)
					returnData = [title, artist, ' ', ' ']
			else:
				#It's not playing a web-stream, but a music file
				print("ITS A FILE!")
				title = currentSong['title']
				artist = currentSong['artist']
				album = currentSong['album']
				#TODO: search for currentSong's elapsedTime in the dict someday.
		else:
			#Volumio is not playing any music at all
			returnData = ['Stopped',' ',' ',' ']
	else:
		# I just need an extra line here, just to avoid KeyErrors
		returnData = ['Title not (yet)','found',' ',' ']
		#title = currentSong['title']
		#artist = currentSong['artist']
		#album = currentSong['album']
		#print(str(title))
		#print(str(artist))
		#print(str(album))
		#print(str(currentSong))
	return returnData

try:
	
	restartLineOne = time()-1
	restartLineTwo = time()-1
	restartLineThree = time()-1
	restartLineFour = time()-1

	posLineOne=0
	posLineTwo=0
	posLineThree=0
	posLineFour=0

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
		if(time()-infoRefreshTimeStamp >= 0.2):
			# It's time to update the information about the songs and such
			songInfo = updateLCDinfo()
			print(str(songInfo))
			# TODO extract useful info from LIST(songInfo)
			textOne = songInfo[0]
			textTwo = songInfo[1]
			textThree = songInfo[2]
			textFour = songInfo[3]

			newTextLineOne =   textOne + " | " + textOne[0:20]
			newTextLineTwo =   textTwo + " | " + textTwo[0:20]
			newTextLineThree = textThree + " | " + textThree[0:20]
			newTextLineFour =  textFour + " | " + textFour[0:20]
			#Now check for any changes
			if(textLineOne != newTextLineOne):
				# Update the text, because there is new text
				textLineOne = newTextLineOne
				# Now reset some int's and bool's to make the text start scolling from the beginning
				posLineOne = 1
				lineOneChanged = True
				writeLineOne = True
				newTextLineOne = True
			if(textLineTwo != newTextLineTwo):
				# Update the text, because there is new text
				textLineTwo = newTextLineTwo
				# Now reset some int's and bool's to make the text start scolling from the beginning
				posLineTwo = 1
				lineTwoChanged = True
				writeLineTwo = True
				newTextLineTwo = True

			#TODO: MORE CHECKZ
			infoRefreshTimeStamp = time()

		#currentSong = client.currentsong()
		#print(str(currentSong))
		if(time()-timeWaitTimeStamp >= timeWait):
			# Line one code starts here
			if(len(textOne) > 20):
				if(time()-restartLineOne > lineTimeWait):
					writeLineOne = True
					toPrintTextLineOne = textLineOne[posLineOne:posLineOne+20]
					lastPrintedTextLineOne = textLineOne[posLineOne:posLineOne+20]
					posLineOne = posLineOne + moveText
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
					posLineTwo = posLineTwo + moveText
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
					posLineThree = posLineThree + moveText
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
					posLineFour = posLineFour + moveText
					lineFourChanged = True
					if(posLineFour >= len(textLineFour)-18):
						posLineFour = 1
						restartLineFour = time()
						lineFourChanged = False
					timeStampLineFour = time()
			else:
				toPrintTextLineFour = textFour
				writeLineFour = True
			
			# Check what stuff to send to the LCD and what to leave out because it's already being displayed
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
except KeyboardInterrupt:
	print("\nExiting...")
