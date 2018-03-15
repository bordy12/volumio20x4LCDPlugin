# Import useful modules
from mpd import MPDClient
import os
import json
import socket

# This class will handle the retreivement of all the music-info if there is new info
class MusicInfo():
    # Constructor
    def __init__(self):
        self.info = {}
	self.info['title'] = ' '
	self.info['artist'] = ' '
	self.info['album'] = ' '
	self.info['trackType'] = ' '
	self.info['status'] = ' '

    # Use volumio.sh to check for any updates to Music-info
    def check_for_updates(self):
	current_info = self.info
	# Check if key variables are not None/undefined
	if 'title' not in self.info:
            self.info['title'] = ' '
        if 'artist' not in self.info:
            self.info['artist'] = ' '
        if 'album' not in self.info:
            self.info['album'] = ' '
	if 'trackType' not in self.info:
            self.info['trackType'] = ' '
	if 'status' not in self.info:
            self.info['status'] = ' '
        # retreive new info
        # execute the volumio.sh command and read it's output
        new_info = os.popen('/volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh status').read()
        # Convert the info to a dictionary
        new_info = json.loads(new_info)
	print('\n\n' + str(new_info))
	# Check if key variables are not None/undefined
        if 'title' not in new_info:
            new_info['title'] = ' '
        if 'artist' not in new_info:
            new_info['artist'] = ' '
        if 'album' not in new_info:
            new_info['album'] = ' '
        if 'trackType' not in new_info:
            new_info['trackType'] = ' '
        if 'status' not in new_info:
            new_info['status'] = ' '
        # Check if the title has changed
        if(new_info['title'] != current_info['title']):
            # The info has changed, return the new info
	    if new_info['title'] is None:
		new_info['title'] = ' '
	    self.info = new_info
            return True
        elif(new_info['artist'] != current_info['artist']):
            # The info has changed, return the new info
	    if new_info['artist'] is None:
                new_info['artist'] = ' '
            self.info = new_info
            return True
        elif(new_info['album'] != current_info['album']):
            # The info has changed, return the new info
	    if new_info['album'] is None:
                new_info['album'] = ' '
            self.info = new_info
	    return True
        elif(new_info['trackType'] != current_info['trackType']):
            # The info has changed, return the new info
            self.info = new_info
            return True
	elif(new_info['status'] != current_info['status']):
            # The info has changed, return the new info
            self.info = new_info
            return True
        else:
            # Nothing important changed, return False
            return False

    def retreive(self):
        if(self.info == ' '):
            # execute the volumio.sh command and read it's output
            self.info = os.popen('/volumio/app/plugins/system_controller/volumio_command_line_client/volumio.sh status').read()
            # Convert the info to a dictionary
            self.info = json.loads(self.info)
	    # Check for empty values before returning them, to prevent errors
	    if 'title' not in self.info:
		self.info['title'] = ' '
	    if 'artist' not in self.info:
		self.info['artist'] = ' '
	    if 'album' not in self.info:
		self.info['album'] = ' '
            # return the info
            return self.info
        else:
	    # return the info
	    if 'title' not in self.info:
                self.info['title'] = ' '
            if 'artist' not in self.info:
                self.info['artist'] = ' '
            if 'album' not in self.info:
                self.info['album'] = ' '
            return self.info
        
    def split_text(self, title):
    	if " - " in title:
    	    return title.split(' - ', 1)
    	elif '-' in title:
    	    return title.split('-', 1)
    	else:
    	    return title


class Settings():
    # constructor
    def __init__(self):
        self.info = ' '


    # Retreive the right config.json and convert it into a python dictionary
    def retreive(self):
        if(os.path.isfile('/data/configuration/user_interface/lcdcontroller/config.json')):
                # There is a config.json created by the UIconfig settings-page. Use that one!
                # Read config.json
                settings_file = open('/data/configuration/user_interface/lcdcontroller/config.json')
                settings_file_content = settings_file.read()
                # Convert it's JSON content into a python-dictionary
                settings_dictionary = json.loads(settings_file_content)
                return settings_dictionary
        elif(os.path.isfile('/data/plugins/user_interface/lcdcontroller/config.json')):
                # Use the config.json that came with the plugin
                # Read config.json
                settings_file = open('/data/plugins/user_interface/lcdcontroller/config.json')
                settings_file_content = settings_file.read()
                # Convert it's JSON content into a python-dictionary
                settings_dictionary = json.loads(settings_file_content)
                return settings_dictionary
        else:
            # There is no config.json. This should not be happening. Exit the python script before it crashes or does something unexpected.
                print("No config.json found!\nExiting...")
                exit(1)

    # validate the settings and return a validated settings-dictionary
    def validate(self, settings_dict):
        settings = settings_dict
        if(len(settings_dict) > 0):

            # Check all settings for potential errors
            try:
                val = int(settings['config_welcome_message_duration']['value'])
            except ValueError:
                settings['config_welcome_message_duration']['value'] = 3
            if(len(settings['config_welcome_message_string_one']['value']) > 20):
                # Welcome message line 1 is too long for the LCD. Cut it off
                settings['config_welcome_message_string_one']['value'] = settings['config_welcome_message_string_one']['value'][0:20]
            if(len(settings['config_welcome_message_string_two']['value']) > 20):
                # Welcome message line 1 is too long for the LCD. Cut it off
                settings['config_welcome_message_string_two']['value'] = settings['config_welcome_message_string_two']['value'][0:20]
            if(len(settings['config_welcome_message_string_three']['value']) > 20):
                # Welcome message line 1 is too long for the LCD. Cut it off
                settings['config_welcome_message_string_three']['value'] = settings['config_welcome_message_string_three']['value'][0:20]
            if(len(settings['config_welcome_message_string_four']['value']) > 20):
                # Welcome message line 1 is too long for the LCD. Cut it off
                print("config_welcome_message_string_four is too long, it has been cut off")
                settings['config_welcome_message_string_four']['value'] = settings['config_welcome_message_string_four']['value'][0:20]

            # Test if the user has enetered a valid IP-addres, either IPv4, IPv6 or the word localhost
            ip = settings['config_host']['value']
            if(len(ip) <= 0):
                settings['config_host']['value'] = 'localhost'
            elif(ip != 'localhost'):
                try:
                    # test for IPv4
                    socket.inet_pton(socket.AF_INET, ip)
                    print("MPD-host setting is recognized as IPv4")
                except socket.error:
                    try:
                        # test for IPv6
                        socket.inet_pton(socket.AF_INET6, ip)
                        print("MPD-host setting is recognized as IPv6")
                    except socket.error:
                        print("mpd_host_setting NOT ok: not 'localhost' or IPv4 or IPv6" + str(ip) + "\nDefaulting to localhost...");
                        settings['config_host']['value'] = 'localhost'

            # Perform some checks to see if the settings are in the right format/type and are not empty
            if(len(settings['config_text_split_string']['value']) <= 0):
                print("config_text_split_string was left empty: Replacing the empty setting with two spaces")
                settings['config_text_split_string']['value'] = '  '
            else:
                if(settings['config_text_split_string']['value'][-1:] != ' ' and settings['config_text_split_string']['value'][0] != ' '):
                    # Add two spaces to this setting, as it looks better
                    settings['config_text_split_string']['value'] = ' ' + str(settings['config_text_split_string']['value']) + ' '
            if(len(settings['config_welcome_message_duration']['value']) <= 0):
                settings['config_welcome_message_duration' ]= ' '
            if(len(str(settings['config_welcome_message_duration']['value'])) < 1):
                # I don't know what the user want when they leave the input field for welcome_message_duration empty or enter non-int chars, so I'll just turn the feature off
                settings['config_welcome_message_duration']['value'] = 0
                settings['config_welcome_message_bool']['value'] = False
            elif(type(settings['config_welcome_message_duration']['value']) != int):
                # Try to convert the setting into an int
                try:
                        settings['config_welcome_message_duration']['value'] = int(settings['config_welcome_message_duration']['value'])
                except:
                        # The setting could not be converted to an int, turn it off
                        settings['config_welcome_message_duration']['value'] = 0
                        settings['config_welcome_message_bool']['value'] = False
            if(settings['config_welcome_message_bool']['value'] == 'true' or settings['config_welcome_message_bool']['value'] == 'True'):
                settings['config_welcome_message_bool']['value'] = True
            elif(settings['config_welcome_message_bool']['value'] == 'false' or settings['config_welcome_message_bool']['value'] == 'False'):
                settings['config_welcome_message_bool']['value'] = False

            # Check the length of messages
            if(len(settings['config_welcome_message_string_one']['value']) <= 0):
                settings['config_welcome_message_string_one']['value'] = ' '
            elif(len(settings['config_welcome_message_string_one']['value']) > 20):
                settings['config_welcome_message_string_one']['value'] = settings['config_welcome_message_string_one']['value'][:20]
            if(len(settings['config_welcome_message_string_two']['value']) <= 0):
                settings['config_welcome_message_string_two']['value'] = ' '
            elif(len(settings['config_welcome_message_string_two']['value']) > 20):
                settings['config_welcome_message_string_two']['value'] = settings['config_welcome_message_string_two']['value'][:20]
            if(len(settings['config_welcome_message_string_three']['value']) <= 0):
                settings['config_welcome_message_string_three']['value'] = ' '
            elif(len(settings['config_welcome_message_string_three']['value']) > 20):
                settings['config_welcome_message_string_three']['value'] = settings['config_welcome_message_string_three']['value'][:20]
            if(len(settings['config_welcome_message_string_four']['value']) <= 0):
                settings['config_welcome_message_string_four']['value'] = ' '
            elif(len(settings['config_welcome_message_string_four']['value']) > 20):
                settings['config_welcome_message_string_four']['value'] = settings['config_welcome_message_string_four']['value'][:20]

            # return validated settings dictionary
            return settings
        else:
            return False
