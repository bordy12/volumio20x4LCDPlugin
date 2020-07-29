#! /usr/bin/env python

#http://www.martyncurrey.com/arduino-with-hd44780-based-lcds/

#Import libraries to manage xml wh forecast
import urllib2
import xml.etree.ElementTree as ET

# Import settings.py (settings.py is stored in the same folder as this file and contains a function that converts the config.json into a python dictionary)
import functions
# Import other useful modules
#from os import *
import os
from time import *
from sys import *
from math import *
from datetime import datetime

#import LCD-related python libs
from I2C_LCD_driver import lcd

#make lcd-positions work properly
lcd_position=[1,3,2,4]

#define lcd length
lcd_lenght = 20

# define some options
timeWaitRefreshLcd = 0.8 # Time in seconds, refresh the LCD every x seconds (if any changes is detected)
lastRefreshTimestamp = time() # This variable needs to be initialized with the value of time()
emptyText = ' '.ljust(lcd_lenght)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Edit the script below to meets your needs
# Il bollettino viene emesso ogni giorno alle ore 13 con aggiornamenti alle ore 16 e alle ore 9
# della mattina seguente. Gli aggiornamenti previsionali si riferiscono alla giornata in corso.
# https://www.arpa.veneto.it/previsioni/it/xml/bollettino_utenti.xml
timeWaitBeforeWhForecast = 40	# Time (in seconds) to wait before displaying the weather forecast
timeShowWhForecast = 10			# Time (in seconds) to wait after the weather forecast is displayed
xml_file = "/home/volumio/bollettino_utenti.xml"	# XML file
xml_tappo = "/home/volumio/bollettino_utenti.tappo"	# If tappo file exists cron is still dowloading the xml
lastForecastTimestamp = time()						# Last time we displayed the w.forecast
forecastSheet = 1
xml_days = ["lun","mar","mer","gio","ven","sab","dom"]

# Icons below are made of 3x2 chars 
# 1. Cloudy w. icon
ico01_idx = ['a5','a6']
ico01 = [ 
[0x00,0x00,0x00,0x00,0x01,0x03,0x03,0x06], 
[0x00,0x00,0x00,0x1F,0x1F,0x00,0x00,0x00], 
[0x00,0x00,0x00,0x00,0x10,0x18,0x18,0xC], 
[0xC,0x18,0x18,0x18,0xF,0x07,0x00,0x00], 
[0x00,0x00,0x00,0x00,0x1F,0x1F,0x00,0x00], 
[0x06,0x03,0x03,0x03,0x1E,0x1C,0x00,0x00], 
]


# 2. Variable w. icon, no rain/snow
ico02_idx = ['a2','a3','a4']
ico02 = [ 
[0x00,0x00,0x00,0x01,0x00,0x00,0x01,0x03], 
[0x11,0x09,0x07,0x18,0x08,0x1F,0x1F,0x00], 
[0x04,0x08,0x10,0xE,0x08,0x14,0x10,0x18], 
[0x03,0x06,0xC,0x18,0x18,0x18,0xF,0x07], 
[0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0x1F], 
[0x18,0xC,0x06,0x03,0x03,0x03,0x1E,0x1C], 
]


# 3. Sunny w. icon
ico03_idx = ['a1']
ico03 = [ 
[0x00,0x00,0x08,0x04,0x03,0x03,0x1E,0x06], 
[0x00,0x11,0x11,0x1F,0x1F,0x00,0x00,0x00], 
[0x00,0x00,0x02,0x04,0x18,0x18,0xF,0xC], 
[0x06,0x1E,0x03,0x03,0x04,0x08,0x00,0x00], 
[0x00,0x00,0x00,0x1F,0x1F,0x11,0x11,0x00], 
[0xC,0xF,0x18,0x18,0x04,0x02,0x00,0x00], 
]


# 4. Variable w. icon, with rain/snow
ico04_idx = ['b1','b2','b5','b6','b8','b9','c1','c2','c5','c6','c8','c9','d1','d2','d5','d6','d8','d9','e1','e2','e5','e6','e8','e9']
ico04 = [ 
[0x00,0x00,0x00,0x01,0x00,0x00,0x01,0x03], 
[0x11,0x09,0x07,0x18,0x08,0x17,0x1F,0x00], 
[0x04,0x08,0x10,0xE,0x08,0x10,0x18,0x18], 
[0x02,0x06,0xC,0x18,0x1F,0xD,0x04,0x02], 
[0x00,0x00,0x00,0x00,0x1F,0x16,0x12,0x09], 
[0x08,0xC,0x06,0x03,0x1F,0x1A,0x08,0x04], 
]


# 5. Rainy w. icon
ico05_idx = ['b3','b4','b7','b10','c3','c7','c10','d3','d4','d7','d10','e3','e4','e7','e10']
ico05 = [ 
[0x00,0x00,0x01,0x03,0x03,0x06,0xC,0x18], 
[0x00,0x1F,0x1F,0x00,0x00,0x00,0x00,0x00], 
[0x00,0x00,0x10,0x18,0x18,0xC,0x06,0x03], 
[0x18,0x18,0xF,0x07,0x02,0x01,0x00,0x00], 
[0x00,0x00,0x1F,0x1F,0x09,0x04,0x12,0x00], 
[0x03,0x03,0x1E,0x1C,0x04,0x12,0x09,0x00], 
]


# 6. Foggy w. icon
ico06_idx = ['f1','f2','f3','f4']
ico06 = [ 
[0x00,0x00,0x00,0x1F,0x1F,0x00,0x00,0x1F], 
[0x00,0x00,0x00,0x1F,0x1F,0x00,0x00,0x1F], 
[0x00,0x00,0x00,0x1F,0x1F,0x00,0x00,0x1F], 
[0x1F,0x00,0x00,0x1F,0x1F,0x00,0x00,0x00], 
[0x1F,0x00,0x00,0x1F,0x1F,0x00,0x00,0x00], 
[0x1F,0x00,0x00,0x1F,0x1F,0x00,0x00,0x00], 
]

# 7 Drop icon
ico07 = [ 
[0x04,0x04,0xE,0xE,0x1F,0x1D,0x1F,0xE], 
]

# 8 Temperature icon
ico08 = [ 
[0x04,0xA,0xA,0xE,0xE,0x1F,0x1B,0xE], 
]
# Some hints for displaying text to a 20x4 lcd
# pos 1,1 = 0x80
# pos 2,1 = 0x80 + 0x40
# pos 3,1 = 0x80 + 0x14
# pos 4,1 = 0x80 + 0x54
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Make sure all the functions are ready for to execute
music_info = functions.MusicInfo()
other_info = functions.OtherInfo()
settings = functions.Settings()

while(True):
	try:
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
		lcd_address = int(plugin_settings['config_lcd_address']['value'],16)
		weather_forecast_bool_setting = plugin_settings['config_weather_forecast_bool']['value']
		break
	except:
		print("Starting up...")

#make sure python knows what an LCD is
my_lcd = lcd(lcd_address)


# Make sure the script doesn't throw errors
songInfo=[' ', ' ', ' ',' ']
textOne = ' '
textTwo = ' '
textThree = ' '
textFour = ' '


def sendToLCD(lineNum, textToDisplay): #This function will send a string to the LCD screen
	my_lcd.lcd_display_string(textToDisplay, lcd_position[lineNum])

def sendToLCD_Centered(lineNum, textToDisplay): #This function will send a string to the LCD screen and centering it
	ll = len(textToDisplay)
	centeredText = textToDisplay
	if(ll < lcd_lenght):
		centeredText = textToDisplay.center(lcd_lenght)
	my_lcd.lcd_display_string(centeredText, lcd_position[lineNum])

# Initialize the LCD to make sure the it always displays normal text instead of garbage
my_lcd.lcd_clear()

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
	LCD_line_one_scroll_counter = lcd_lenght
	LCD_line_two_scroll_counter = lcd_lenght
	LCD_line_three_scroll_counter = lcd_lenght
	LCD_line_four_scroll_counter = lcd_lenght

	LCD_line_one_text_sent = "."
	LCD_line_two_text_sent = "."
	LCD_line_three_text_sent = "."
	LCD_line_four_text_sent = "."

	LCD_line_one = ' '
	LCD_line_two = ' '
	LCD_line_three = ' '
	LCD_line_four = ' '

	todayDateStr = ' '

	# retreive some useful info
	info = music_info.retreive()
	title = info['title']
	artist = info['artist']
	album = info['album']
	trackType = info['trackType']
	status = info['status']

	oinfo = other_info.retreive()
	volume = str(oinfo['volume'])
	last_volume = volume

	title_splitter_found = False

	my_lcd.lcd_clear()

	while(True):
		sleep(timeWaitRefreshLcd)

		if weather_forecast_bool_setting:
			if(time() > lastForecastTimestamp + timeWaitBeforeWhForecast):
				lastForecastTimestamp = time()
				if not os.path.exists(xml_tappo):
					if os.path.exists(xml_file):
						if os.stat(xml_file).st_size != 0:
							#Load wh forecast from xml file on disk
							dati_analisi=ET.parse(xml_file)
							base_dati = dati_analisi.getroot()

							# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
							# Edit the script below to meets your needs
							h = datetime.now().hour
							xml_today = datetime.now().weekday()
							xml_tomorrow = (0, xml_today + 1)[xml_today + 1 < 6]
							meteogrammiTV = base_dati.find("meteogrammi/meteogramma/[@name='Treviso e pianura orientale']")
							for meteogramma in meteogrammiTV:
								scadenza = meteogramma.attrib["data"]
								for meteogramma_dett in meteogramma:
									value = meteogramma_dett.get('title')
									if(value=="Simbolo"):
										idx_ico = meteogramma_dett.attrib["value"][-6:][:2]
									if(value=="Temperatura"):
										temperatura = meteogramma_dett.attrib["value"]
									if(value=="Probabilita' precipitazione"):
										precipitazioni = meteogramma_dett.attrib["value"]
										precipitazioni_val = 0
										if(precipitazioni):
											precipitazioni_val = int(precipitazioni.replace("%",""))
								if(forecastSheet == 1):
									if(xml_days[xml_today] == scadenza[:3]):
										if(h <= 12 and scadenza.find("mattina") > 0):
											break
										elif(h > 12 and scadenza.find("pomeriggio") > 0):
											break
										elif(scadenza.find("mattina") < 0 and scadenza.find("pomeriggio") < 0):
											break
								if(forecastSheet == 2):
									if(xml_days[xml_today] == scadenza[:3]):
										if(h <= 12 and scadenza.find("pomeriggio") > 0):
											break
										elif(scadenza.find("mattina") < 0 and scadenza.find("pomeriggio") < 0):
											break
									if(xml_days[xml_tomorrow] == scadenza[:3]):
										if(h > 12 and scadenza.find("mattina") > 0):
											break
										elif(scadenza.find("mattina") < 0 and scadenza.find("pomeriggio") < 0):
											break
								if(forecastSheet == 3):
									if(xml_days[xml_tomorrow] == scadenza[:3]):
										if(h <= 12 and scadenza.find("mattina") > 0):
											break
										if(h > 12 and scadenza.find("pomeriggio") > 0):
											break
										elif(scadenza.find("mattina") < 0 and scadenza.find("pomeriggio") < 0):
											break
							if(idx_ico in ico01_idx):
								my_lcd.lcd_load_custom_chars(ico01 + ico07 + ico08)
							if(idx_ico in ico02_idx):
								my_lcd.lcd_load_custom_chars(ico02 + ico07 + ico08)
							if(idx_ico in ico03_idx):
								my_lcd.lcd_load_custom_chars(ico03 + ico07 + ico08)
							if(idx_ico in ico04_idx):
								my_lcd.lcd_load_custom_chars(ico04 + ico07 + ico08)
							if(idx_ico in ico05_idx):
								my_lcd.lcd_load_custom_chars(ico05 + ico07 + ico08)
							if(idx_ico in ico06_idx):
								my_lcd.lcd_load_custom_chars(ico06 + ico07 + ico08)
							my_lcd.lcd_clear()
							# Write first three icon's chars to row 3, col 2 directly
							my_lcd.lcd_write(0x80 + 0x15)
							my_lcd.lcd_write_char(0)
							my_lcd.lcd_write_char(1)
							my_lcd.lcd_write_char(2)
							# Write next three icon's chars to row 4, col 2 directly
							my_lcd.lcd_write(0x80 + 0x55)
							my_lcd.lcd_write_char(3)
							my_lcd.lcd_write_char(4)
							my_lcd.lcd_write_char(5)
							# Display wheather forecast from xml
							my_lcd.lcd_display_string(scadenza[:20].upper(),1,0)
							if(idx_ico[:1] == "c"):
								my_lcd.lcd_display_string("*Temporali*",2,0)
								my_lcd.lcd_display_string(str(forecastSheet) + "/3",2,17)
							elif(idx_ico[:1] == "d"):
								my_lcd.lcd_display_string("*Neve*",2,0)
								my_lcd.lcd_display_string(str(forecastSheet) + "/3",2,17)
							elif(idx_ico[:1] == "e"):
								my_lcd.lcd_display_string("*Neve e Pioggia*",2,0)
								my_lcd.lcd_display_string(str(forecastSheet) + "/3",2,17)
							else:
								my_lcd.lcd_display_string(str(forecastSheet) + "/3",2,8)
							my_lcd.lcd_display_string(temperatura.upper(),4,8)
							if(precipitazioni_val > 0):
								my_lcd.lcd_display_string("PROB. "+precipitazioni,3,8)
								my_lcd.lcd_write(0x80 + 0x1A)
								my_lcd.lcd_write_char(6)
							my_lcd.lcd_write(0x80 + 0x5A)
							my_lcd.lcd_write_char(7)
							forecastSheet += 1
							if(forecastSheet > 3):
								forecastSheet = 1
							sleep(timeShowWhForecast)
							my_lcd.lcd_clear()
							LCD_line_one_text_sent = "."
							LCD_line_two_text_sent = "."
							LCD_line_three_text_sent = "."
							LCD_line_four_text_sent = "."
							# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

		today = datetime.now()
		todayDateStr = today.strftime("%d.%m.%Y %H:%M")
		LCD_line_four = todayDateStr

		if(other_info.check_for_updates() !=  False):
			oinfo = other_info.retreive()
			volume = str(oinfo['volume'])

		if(volume != last_volume):
			last_volume = volume
			LCD_line_four = "Volume: " + volume + "%"
			sendToLCD_Centered(3, LCD_line_four)
			LCD_line_four_text_sent = LCD_line_four

		#Do not resend any previously sent text
		if(LCD_line_four_text_sent != LCD_line_four):
			sendToLCD_Centered(3, LCD_line_four)
			LCD_line_four_text_sent = LCD_line_four

		# Check for updates on the information we have
		if(music_info.check_for_updates() !=  False):
			# Looks like there is an update to the info we have, update everything and reset scroll-counters
			info = music_info.retreive()
			LCD_line_one_scroll_counter = lcd_lenght
			LCD_line_two_scroll_counter = lcd_lenght
			LCD_line_three_scroll_counter = lcd_lenght

			#clean-up lcd and reset last sent lines to lcd
			sendToLCD(0, emptyText)
			sendToLCD(1, emptyText)
			sendToLCD(2, emptyText)
			LCD_line_one_text_sent = "."
			LCD_line_two_text_sent = "."
			LCD_line_three_text_sent = "."

		title = str(info['title'])
		artist = str(info['artist'])
		album = str(info['album'])
		trackType = str(info['trackType'])
		status = str(info['status'])
		
		if(str(trackType) == 'webradio' and status != 'stop'):
			# Webradio's always display their song-info in the title-value and their radio station in the artist-value,
			# This creates a small problem: <song name>-<song artist> is a one-liner. This text needs to be split into 2 lines
			# This for-loop starts at 1 and ends at title-1, because i want to ignore any '-' at the beginning and end of the 'title'

			title = music_info.split_text(title)
			if(status == 'play'):
				# Display information about current webradio music
				if(type(title) == list and len(title) == 2):
					LCD_line_one = str(title[0])
					LCD_line_two = str(title[1])
					LCD_line_three = str(artist)
				else:
					LCD_line_one = str(title)
					LCD_line_two = str(artist)
					LCD_line_three = ' '

		elif(str(trackType) != 'webradio' and status != 'stop'):
			# If every information we need is present, display it
			if(len(str(title)) > 0 and len(str(artist)) > 0 and len(str(album)) > 0):
				LCD_line_one = str(title)
				LCD_line_two = str(artist)
				if(len(str(album)) > 0):
					LCD_line_three = str(album)
				else:
					LCD_line_three = " "
			# If some information is present, display it
			elif(len(str(title)) > 0 and len(str(artist)) > 0):
				LCD_line_one = str(title)
				LCD_line_two = str(artist)
				if(len(str(album)) > 0):
					LCD_line_three = str(album)
				else:
					LCD_line_three = " "
			# If no info is present, do some funky stuff to the info, like remove .mp3/.wma/1./etc
			elif(len(str(title)) > 0 and len(str(artist)) <= 0):
				title = title.replace(".mp3", "").replace(".wma", "").replace(".flac", "").replace(". ", "")
				try:
					while(True):
						int(title[0])
						title = title[1::]
				except:
					print("\n")
				
				title = music_info.split_text(title)
				if(len(str(title[1])) > 0):
					LCD_line_one = str(title[0])
					LCD_line_two = str(title[1])
					if(len(str(album)) > 0):
						LCD_line_three = str(album)
					else:
						LCD_line_three = " "

		else:
			LCD_line_one = " "
			LCD_line_two = " "
			LCD_line_three = " "

		# Fix types in case they have weird types like chars/arrays
		LCD_line_one = str(LCD_line_one)
		LCD_line_two = str(LCD_line_two)
		LCD_line_three = str(LCD_line_three)

		# The following lines of code handle the output to the first line of the LCD
		if(len(LCD_line_one) > lcd_lenght):
			if text_split_string_setting not in LCD_line_one:
				#Add text-separator to text
				LCD_line_one = LCD_line_one + str(text_split_string_setting)
				# Scroll the first part of the text
			if(LCD_line_one_scroll_counter<len(LCD_line_one)):
				sendToLCD(0, LCD_line_one[LCD_line_one_scroll_counter-lcd_lenght:LCD_line_one_scroll_counter])
				LCD_line_one_scroll_counter+=1
				# Make sure the text reaches the beginning again
			else:
				# If text reached the beginning again, set the counter to initial value 20, NOT 0 (zero)
				if(len(LCD_line_one[LCD_line_one_scroll_counter-lcd_lenght:]) <= 0):
					LCD_line_one_scroll_counter = lcd_lenght
				# if the text reaches the end, do some magic to make te look like it scrolls through
				else:
					sendToLCD(0, LCD_line_one[LCD_line_one_scroll_counter-lcd_lenght:] + LCD_line_one[0:LCD_line_one_scroll_counter-len(LCD_line_one)])
					LCD_line_one_scroll_counter+=1
		else:
			# Do not resend any previously sent text
			if(LCD_line_one_text_sent != LCD_line_one):
				sendToLCD_Centered(0, LCD_line_one)
				LCD_line_one_text_sent = LCD_line_one
		# The following lines of code handle the output to the second line of the LCD
		if(len(LCD_line_two) > lcd_lenght):
			if text_split_string_setting not in LCD_line_two:
				#Add text-separator to text
				LCD_line_two = LCD_line_two + str(text_split_string_setting)
					# Scroll the first part of the text
				if(LCD_line_two_scroll_counter<len(LCD_line_two)):
					sendToLCD(1, LCD_line_two[LCD_line_two_scroll_counter-lcd_lenght:LCD_line_two_scroll_counter])
					LCD_line_two_scroll_counter+=1
					# Make sure the text reaches the beginning again
				else:
					# If text reached the beginning again, set the counter to initial value 20, NOT 0 (zero)
					if(len(LCD_line_two[LCD_line_two_scroll_counter-lcd_lenght:]) <= 0):
						LCD_line_two_scroll_counter = lcd_lenght
					# if the text reaches the end, do some magic to make te look like it scrolls through
					else:
						sendToLCD(1, LCD_line_two[LCD_line_two_scroll_counter-lcd_lenght:] + LCD_line_two[0:LCD_line_two_scroll_counter-len(LCD_line_two)])
						LCD_line_two_scroll_counter+=1
		else:
			# Do not resend any previously sent text
			if(LCD_line_two_text_sent != LCD_line_two):
				sendToLCD_Centered(1, LCD_line_two)
				LCD_line_two_text_sent = LCD_line_two
		# The following lines of code handle the output to the third line of the LCD
		if(len(LCD_line_three) > lcd_lenght):
			if text_split_string_setting not in LCD_line_three:
				#Add text-separator to text
				LCD_line_three = LCD_line_three + str(text_split_string_setting)
				# Scroll the first part of the text
				if(LCD_line_three_scroll_counter<len(LCD_line_three)):
					sendToLCD(2, LCD_line_three[LCD_line_three_scroll_counter-lcd_lenght:LCD_line_three_scroll_counter])
					LCD_line_three_scroll_counter+=1
				# Make sure the text reaches the beginning again
				else:
					# If text reached the beginning again, set the counter to initial value 20, NOT 0 (zero)
					if(len(LCD_line_three[LCD_line_three_scroll_counter-lcd_lenght:]) <= 0):
						LCD_line_three_scroll_counter = lcd_lenght
					# if the text reaches the end, do some magic to make te look like it scrolls through
					else:
						sendToLCD(2, LCD_line_three[LCD_line_three_scroll_counter-lcd_lenght:] + LCD_line_three[0:LCD_line_three_scroll_counter-len(LCD_line_three)])
						LCD_line_three_scroll_counter+=1
		else:
			# Do not resend any previously sent text
			if(LCD_line_three_text_sent != LCD_line_three):
				sendToLCD_Centered(2, LCD_line_three)
				LCD_line_three_text_sent = LCD_line_three

except KeyboardInterrupt:
	print('\nCtrl-C caught\nExiting')
	exit(0)
