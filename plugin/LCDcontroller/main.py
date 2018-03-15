#! /usr/bin/env python

# Import settings.py (settings.py is stored in the same folder as this file and contains a function that converts the config.json into a python dictionary)
import functions
# Import other useful modules
from os import *
from time import *
from sys import *
from math import *

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

# Initialize the LCD to make sure the it always displays normal text instead of garbage
sendToLCD(0, ' ')
sendToLCD(1, ' ')
sendToLCD(2, ' ')
sendToLCD(3, ' ')

# Make sure all the functions are ready for to execute
music_info = functions.MusicInfo()
settings = functions.Settings()

plugin_settings = settings.retreive()
plugin_settings = settings.validate(plugin_settings)
# Extract all the settings into variables
welcome_message_bool_setting = plugin_settings['config_welcome_message_bool']['value']
welcome_message_string_one_setting = plugin_settings['config_welcome_message_string_one']['value']
welcome_message_string_two_setting = plugin_settings['config_welcome_message_string_two']['value']
welcome_message_string_three_setting = plugin_settings['config_welcome_message_string_three']['value']
welcome_message_string_four_setting = plugin_settings['config_welcome_message_string_four']['value']
welcome_message_duration_setting = plugin_settings['config_welcome_message_duration']['value']
text_split_string_setting = plugin_settings['config_text_split_string']['value']
text_scroll = plugin_settings['text_scroll']['value']

# Show welcome message if the user enabled the feature
if(welcome_message_bool_setting == True):
        sendToLCD(0, welcome_message_string_one_setting)
        sendToLCD(1, welcome_message_string_two_setting)
        sendToLCD(2, welcome_message_string_three_setting)
        sendToLCD(3, welcome_message_string_four_setting)
        sleep(welcome_message_duration_setting)

# Send text to the LCD-display
try:
        # Pre-define some counters and variables before entering while-loop
        LCD_line_one_scroll_counter = 20
        LCD_line_two_scroll_counter = 20
        LCD_line_three_scroll_counter = 20
        LCD_line_four_scroll_counter = 20

        LCD_line_one_text_sent = False
        LCD_line_two_text_sent = False
        LCD_line_three_text_sent = False
        LCD_line_four_text_sent = False

	LCD_line_one = ' '
	LCD_line_two = ' '
	LCD_line_three = ' '
	LCD_line_four = ' '

        info_configured = False

        # retreive some useful info
        info = music_info.retreive()
        title = info['title']
        artist = info['artist']
        album = info['album']
        trackType = info['trackType']
        status = info['status']
        title_splitter_found = False

        if(len(text_scroll) > 0):
            if(str(text_scroll) == "1"):
                # Value is 1, scroll the text if too long
                while(True):
                    # Check for updates on the information we have
                    if(music_info.check_for_updates() !=  False):
			print('New music-info found: reloading LCD')
			sleep(0.5)
                        # Looks like there is an update to the info we have, update everything and reset scroll-counters
                        info = music_info.retreive()
                        LCD_line_one_scroll_counter = 20
                        LCD_line_two_scroll_counter = 20
                        LCD_line_three_scroll_counter = 20
                        LCD_line_four_scroll_counter = 20
                        # Make sure the new title, artist and album get sent to LCD
                        info_configured = False

                     # Extract title, artist and album from new info
                    if(info_configured == False):
                        title = str(info['title'])
                        artist = str(info['artist'])
                        album = str(info['album'])
			trackType = str(info['trackType'])
			status = str(info['status'])

                    if(str(trackType) == 'webradio' and info_configured == False):
			# Webradio's always display their song-info in the title-value and their radio station in the artist-value,
                        # This creates a small problem: <song name>-<song artist> is a one-liner. This text needs to be split into 2 lines
                        # This for-loop starts at 1 and ends at title-1, because i want to ignore any '-' at the beginning and end of the 'title'
			title = music_info.split_text(title)
			if(status != 'stop'):
			    # Display information about current music
		            if(type(title) == list and len(title) == 2):
				LCD_line_one = str(title[0])
				LCD_line_two = str(title[1])
				LCD_line_three = str(artist)
			    else:
				LCD_line_one = str(title)
				LCD_line_two = str(artist)
				LCD_line_three = ' '
			else:
			    LCD_line_one = ' '
			    LCD_line_two = ' '
			    LCD_line_three = ' '
			


                    elif(str(trackType) != 'webradio' and info_configured == False):
                        # Just make sure the info we send to the LCD is not null
                        if(len(LCD_line_one) != 0):
                            LCD_line_one = title
                        else:
                            LCD_line_one = ' '
                        if(len(LCD_line_two) != 0):
                            LCD_line_two = artist
                        else:
                            LCD_line_two = ' '
                        if(len(LCD_line_three) != 0):
                            LCD_line_three = album
                        else:
                            LCD_line_three = ' '
                        info_configured = True

		    # Fix types
                    LCD_line_one = str(LCD_line_one)
                    LCD_line_two = str(LCD_line_two)
                    LCD_line_three = str(LCD_line_three)
                
                    # The following lines of code handle the output to the first line of the LCD
                    if(len(LCD_line_one) > 20):
			if text_split_string_setting not in LCD_line_one:
			    #Add text-separator to text
			    LCD_line_one = LCD_line_one + str(text_split_string_setting)

                        # Scroll the first part of the text
                        if(LCD_line_one_scroll_counter<len(LCD_line_one)):
                            sendToLCD(0, LCD_line_one[LCD_line_one_scroll_counter-20:LCD_line_one_scroll_counter])
                            LCD_line_one_scroll_counter+=1
                        # Make sure the text reaches the beginning again
                        else:
                            # If text reached the beginning again, set the counter to initial value 20, NOT 0 (zero)
                            if(len(LCD_line_one[LCD_line_one_scroll_counter-20:]) <= 0):
                                LCD_line_one_scroll_counter = 20
                            # if the text reaches the end, do some magic to make te look like it scrolls through
                            else:
                                sendToLCD(0, LCD_line_one[LCD_line_one_scroll_counter-20:] + LCD_line_one[0:LCD_line_one_scroll_counter-len(LCD_line_one)])
                                LCD_line_one_scroll_counter+=1
                    else:
                            # Do not resend any previously sent text
                            if(LCD_line_one_text_sent != LCD_line_one):
                                sendToLCD(0, LCD_line_one)
                                LCD_line_one_text_sent = LCD_line_one
                            # The following lines of code handle the output to the second line of the LCD
                    if(len(LCD_line_two) > 20):
			if text_split_string_setting not in LCD_line_two:
                            #Add text-separator to text
                            LCD_line_two = LCD_line_two + str(text_split_string_setting)

                        # Scroll the first part of the text
                        if(LCD_line_two_scroll_counter<len(LCD_line_two)):
                            sendToLCD(1, LCD_line_two[LCD_line_two_scroll_counter-20:LCD_line_two_scroll_counter])
                            LCD_line_two_scroll_counter+=1
                        # Make sure the text reaches the beginning again
                        else:
                            # If text reached the beginning again, set the counter to initial value 20, NOT 0 (zero)
                            if(len(LCD_line_two[LCD_line_two_scroll_counter-20:]) <= 0):
                                LCD_line_two_scroll_counter = 20
                            # if the text reaches the end, do some magic to make te look like it scrolls through
                            else:
                                sendToLCD(1, LCD_line_two[LCD_line_two_scroll_counter-20:] + LCD_line_two[0:LCD_line_two_scroll_counter-len(LCD_line_two)])
                                LCD_line_two_scroll_counter+=1
                    else:
                            # Do not resend any previously sent text
                            if(LCD_line_two_text_sent != LCD_line_two):
                                sendToLCD(1, LCD_line_two)
                                LCD_line_two_text_sent = LCD_line_two
                            # The following lines of code handle the output to the second line of the LCD

                    if(len(LCD_line_three) > 20):
			if text_split_string_setting not in LCD_line_three:
                            #Add text-separator to text
                            LCD_line_three = LCD_line_three + str(text_split_string_setting)

                        # Scroll the first part of the text
                        if(LCD_line_three_scroll_counter<len(LCD_line_three)):
                            sendToLCD(2, LCD_line_three[LCD_line_three_scroll_counter-20:LCD_line_three_scroll_counter])
                            LCD_line_three_scroll_counter+=1
                        # Make sure the text reaches the beginning again
                        else:
                            # If text reached the beginning again, set the counter to initial value 20, NOT 0 (zero)
                            if(len(LCD_line_three[LCD_line_three_scroll_counter-20:]) <= 0):
                                LCD_line_three_scroll_counter = 20
                            # if the text reaches the end, do some magic to make te look like it scrolls through
                            else:
                                sendToLCD(2, LCD_line_three[LCD_line_three_scroll_counter-20:] + LCD_line_three[0:LCD_line_three_scroll_counter-len(LCD_line_three)])
                                LCD_line_three_scroll_counter+=1
                    else:
                            # Do not resend any previously sent text
                            if(LCD_line_three_text_sent != LCD_line_three):
                                sendToLCD(2, LCD_line_three)
                                LCD_line_three_text_sent = LCD_line_three
		    sleep(1.2)
            elif(str(text_scroll) == "2"):
                # Value is 2, truncate the text
                print('WIP')
            elif(str(text_scroll) != "1" or str(text_scroll) != "2"):
                # Something went VERY wrong, cannot continue
                exit(1)
            else:
                print("\nCannot determine what to do, scroll the text or truncate the text.")
                print("This problem can occur when the current settings-file (config.json) does not contain the new settings entries")
                print("Try deleting '/data/configuration/user_interface/lcdcontroller/config.json' and reconfiguring the plugin settings via the plugin-manager.")


except KeyboardInterrupt:
        print('\nCtrl-C caught\nExiting')
        exit(0)
