import os.path
import json

def getSettings():
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
		exit(1)
