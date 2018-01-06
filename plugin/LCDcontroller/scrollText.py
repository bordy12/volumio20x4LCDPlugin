#! /usr/bin/env python

# Import settings.py (settings.py is stored in the same folder as this file and contains a function that converts the config.json into a python dictionary)
import settings
# Import other useful modules
from os import *
from time import *
from sys import *
from math import *
from mpd import MPDClient

lcd_settings = settings.getSettings() # Ask settings.py for the settings

# Extract all useful settings for this script
text_split_string_setting = lcd_settings['config_text_split_string']['value']
welcome_message_duration_setting = lcd_settings['config_welcome_message_duration']['value']
welcome_message_bool_setting = lcd_settings['config_welcome_message_bool']['value']
welcome_message_string_one_setting = lcd_settings['config_welcome_message_string_one']['value']
welcome_message_string_two_setting = lcd_settings['config_welcome_message_string_two']['value']
welcome_message_string_three_setting = lcd_settings['config_welcome_message_string_three']['value']
welcome_message_string_four_setting = lcd_settings['config_welcome_message_string_four']['value']
mpd_host_setting = lcd_settings['config_host']['value']

# Debug, print all the settings before checking the settings
print('\nBEFORE:\n')
print(text_split_string_setting)
print(welcome_message_duration_setting)
print(welcome_message_bool_setting)
print(welcome_message_string_one_setting)
print(welcome_message_string_two_setting)
print(welcome_message_string_three_setting)
print(welcome_message_string_four_setting)
print(mpd_host_setting)

# Perform some checks to see if the settings are in the right format/type and are not empty
if(len(text_split_string_setting) <= 0):
	text_split_string_setting = '  '
else:
	text_split_string_setting = ' ' + str(text_split_string_setting) + ' '
if(len(welcome_message_duration_setting) <= 0):
	welcome_message_duration_setting = ' '
if(len(str(welcome_message_duration_setting)) < 1):
	# I don't know what the user want when they leave the input field for welcome_message_duration empty or enter non-int chars, so I'll just turn the feature off
	welcome_message_duration_setting = 0
	welcome_message_bool_setting = False
elif(type(welcome_message_duration_setting) != int):
	# Try to convert the setting into an int
	try:
		welcome_message_duration_setting = int(welcome_message_duration_setting)
	except:
		# The setting could not be converted to an int, turn it off
		welcome_message_duration_setting = 0
		welcome_message_bool_setting = False
if(welcome_message_bool_setting == 'true' or welcome_message_bool_setting == 'True'):
	welcome_message_bool_setting = True
elif(welcome_message_bool_setting == 'false' or welcome_message_bool_setting == 'False'):
	welcome_message_bool_setting = False
if(len(welcome_message_string_one_setting) <= 0):
	welcome_message_string_one_setting = ' '
if(len(welcome_message_string_two_setting) <= 0):
	welcome_message_string_two_setting = ' '
if(len(welcome_message_string_three_setting) <= 0):
	welcome_message_string_three_setting = ' '
if(len(welcome_message_string_four_setting) <= 0):
	welcome_message_string_four_setting = ' '
if(len(mpd_host_setting) <= 0):
	# This script NEEDS mpd_host_setting. It cannot be left empty. To avoid errors, set the setting to localhost if no host is configured.
	mpd_host_setting = 'localhost'

# Debug, print all the settings after checking the settings
print('\nAFTER:\n')
print(text_split_string_setting)
print(welcome_message_duration_setting)
print(welcome_message_bool_setting)
print(welcome_message_string_one_setting)
print(welcome_message_string_two_setting)
print(welcome_message_string_three_setting)
print(welcome_message_string_four_setting)
print(mpd_host_setting)

mpd_host = mpd_host_setting
mpd_port = "6600"
mpd_password = "volumio"

client = MPDClient()
client.connect(mpd_host, mpd_port)

#import LCD-related python libs
from lcd_display import lcd

#make sure python knows what an LCD is
my_lcd = lcd()

#make lcd-positions work properly
lcd_position=[1,3,2,4]

# define some options
moveText = 1 # How many characters to move each time. This should remain 1. Also, this should never have a float-value.
infoRefreshTimeWait = 0.4 # How often should the script check for new song-/radio-info (value is in seconds)?
timeWaitTimeStamp = 0 # This variable needs to be initialized with value 0
infoRefreshTimeStamp = time() # This variable needs to be initialized with the value of time()
timeWait = 1 # Amount of time to wait before moving a piece of text on the lcd
lineTimeWait = 0  # Should have a value of 0, unless the moving text should wait extra long before restarting the line-scrolling

# Make sure the script doesn't throw errors
songInfo=[' ', ' ', ' ',' ']
textOne = ' '
textTwo = ' '
textThree = ' '
textFour = ' '

def sendToLCD(lineNum, textToDisplay): #This function will send a string to the LCD screen
        my_lcd.display_string(textToDisplay, lcd_position[lineNum])

welcomeTimestamp = time() # This variable needs to be initialized with the value of time()

# Make sure the LCD displays normal text when spoken to
sendToLCD(0, ' ')
sendToLCD(1, ' ')
sendToLCD(2, ' ')
sendToLCD(3, ' ')

# Show welcome message if the user enabled the feature
if(welcome_message_bool_setting == True):
	sendToLCD(0, welcome_message_string_one_setting)
	sendToLCD(1, welcome_message_string_two_setting)
	sendToLCD(2, welcome_message_string_three_setting)
	sendToLCD(3, welcome_message_string_four_setting)
	sleep(welcome_message_duration_setting)

def updateLCDinfo():
	returnData = [' ', ' ', ' ', ' ']
	currentSong = client.currentsong()
	status = client.status()
	if(status['state'] != 'stop'):
		if(str(currentSong) != '{}'):
			if('file' in str(currentSong)):
				source = currentSong['file']
				if 'http' in currentSong['file']: #Check for any webstreams before returning information
					#It's a radio-stream from the interwebs! Split the title at ' - ' or '-' into multiple lines, because it might contain the artist's name
					radioName = ' '
					extraInfo = ' '
					extraInfoFound = False
					if('name' in str(currentSong)):
						radioName = currentSong['name']
					if('title' in str(currentSong)):
						title = currentSong['title']
					else:
						title = ' '
					if ' - ' in title or ' : ' in title:
						titleSplit = title.replace(' : ', ' - ').split(' - ')
						title = titleSplit[0]
						artist = titleSplit[1]
						if(len(titleSplit) >= 3):
							extraInfo = titleSplit[2]
							extraInfoFound = True
						if(artist[0:1] == ' '):  # split() does it's job correctly, but I don't want a <space> at the beginning of informations
							artist = artist[1::]  # So info=info-first_char
						if(title[-1] == ' '):
							title = title[:-1]
						if(extraInfoFound == False):
							returnData = [title, artist, radioName, ' ']
						else:
							returnData = [title, artist, extraInfo, radioName]
					elif '-' in title or ':' in title:
						titleSplit = title.replace(':', '-').split('-')
						title = titleSplit[0]
						artist = titleSplit[1]
						if(len(titleSplit) >= 3):
							extraInfo = titleSplit[2]
							extraInfoFound = True
						if(artist[0:1] == ' '):  # split() does it's job correctly, but I don't want a <space> at the beginning of informations
							artist = artist[1::]  # So info=info-first_char
						if(title[-1] == ' '):
							title = title[:-1]
						if(extraInfoFound == False):
							returnData = [title, artist, radioName, ' ']
						else:
							returnData = [title, artist, extraInfo, radioName]
					else:
						returnData = [title, radioName, ' ', ' ']
				else:
					# It's not playing a web-stream, but a music file
					# Try to extract as much info as possible from music files, either from reading the tags or from the filename
					artistFoundBySplittingFilename = False
					extraInfo = ' '
					extraInfoFound = False
					albumFound = False
					if 'title' in str(currentSong):
						title = currentSong['title']
					else:
						title = currentSong['file']
						#Do not include .mp3, .wma, .flac etc. in the song's name
						if(str(title[-4]) == '.'):
							title = title[0:-4]
						elif(str(title[-5]) == '.'):
							title = title[0:-5]
						while('USB/' in title):
							title = title[4::] # Remove all the 'USB/' from the filename's path
						while('INTERNAL/' in title):
							title = title[9::] # Remove all the '/INTERNAL' from the filename's path
						if ' - ' in title or ' : ' in title:
							titleSplit = title.replace(' : ', ' - ').split(' - ')
							title = titleSplit[0]
							artist = titleSplit[1]
							#Remove all spaces before and after the title artist text
							if(title[0] == ' '):
								title = title[1::]
							elif(title[-1] == ' '):
								title = title[:-1]
							if(artist[0] == ' '):
								artist = artist[1::]
							elif(artist[-1] == ' '):
								artist = artist[:-1]
							#We already found the artist, stop looking for tags, because the filename might contain more information
							if(artist != '' or artist != ' '):
								artistFoundBySplittingFilename = True
							if(artist[0:1] == ' '):  # split() does it's job correctly, but I don't want a <space> at the beginning of informations
								artist = artist[1::]  # So info=info-first_char
							if(title[-1] == ' '):
								title = title[:-1]
							#Look for more info that might be useful to people, like the album-name
							if(len(titleSplit) >= 3):
								extraInfo = titleSplit[2]
								extraInfoFound = True
					# Check if the file contains an artist-name
					if 'albumartist' in str(currentSong) and artistFoundBySplittingFilename == False:
						artist = currentSong['albumartist']
					elif(artistFoundBySplittingFilename == False):
						artist = ' '
					# Check if the file contains an album-name
					if 'album' in str(currentSong):
						album = currentSong['album']
						albumFound = True
					else:
						album = ' '
					m, s = divmod(float(status['elapsed']), 60)
					h, m = divmod(m, 60)
					elapsedTime = "%d:%02d:%02d" % (h, m, s)
					if(status['state'] == 'pause'):
						elapsedTime = "   " + str(elapsedTime) + " ||"
					if(albumFound == True and extraInfoFound == False):
						returnData = [title, artist, album, str(elapsedTime)]
					else:
						returnData = [title, artist, extraInfo, str(elapsedTime)]
			else:
				returnData = [' ', ' ', ' ', ' ']
		else:
			# There is no info to display, send voids
			returnData = [' ',' ',' ',' ']
	else:
		# Send voids to the display, as nothing is playing at the moment
		returnData = [' ', ' ', ' ', ' ']
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

	textLineOne =   textOne + text_split_string_setting + textOne[0:20]
	textLineTwo =   textTwo + text_split_string_setting + textTwo[0:20]
	textLineThree = textThree + text_split_string_setting + textThree[0:20]
	textLineFour =  textFour + text_split_string_setting + textFour[0:20]
	
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
		if(time()-infoRefreshTimeStamp >= infoRefreshTimeWait):
			# It's time to update the information about the songs and such
			songInfo = updateLCDinfo()
			textOne = songInfo[0]
			textTwo = songInfo[1]
			textThree = songInfo[2]
			textFour = songInfo[3]

			newTextLineOne =   textOne + text_split_string_setting + textOne[0:20]
			newTextLineTwo =   textTwo + text_split_string_setting + textTwo[0:20]
			newTextLineThree = textThree + text_split_string_setting + textThree[0:20]
			newTextLineFour =  textFour + text_split_string_setting + textFour[0:20]
			#Now check for any changes
			if(textLineOne != newTextLineOne):
				# Update the text, because there is new text
				textLineOne = newTextLineOne
				# Now reset some int's and bool's to make the text start scolling from the beginning
				posLineOne = 0
				lineOneChanged = True
				writeLineOne = True
				newTextLineOne = True
			if(textLineTwo != newTextLineTwo):
				# Update the text, because there is new text
				textLineTwo = newTextLineTwo
				# Now reset some int's and bool's to make the text start scolling from the beginning
				posLineTwo = 0
				lineTwoChanged = True
				writeLineTwo = True
				newTextLineTwo = True
			if(textLineThree != newTextLineThree):
				# Update the text, because there is new text
				textLineThree = newTextLineThree
				# Now reset some int's and bool's to make the text start scolling from the beginning
				posLineThree = 0
				lineThreeChanged = True
				writeLineThree = True
				newTextLineThree = True
			if(textLineFour != newTextLineFour):
				# Update the text, because there is new text
				textLineFour = newTextLineFour
				# Now reset some int's and bool's to make the text start scolling from the beginning
				posLineFour = 0
				lineFourChanged = True
				writeLineFour = True
				newTextLineFour = True
			# Set a new time to check for changes in text
			infoRefreshTimeStamp = time()

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
