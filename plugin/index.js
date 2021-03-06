'use strict';

var libQ = require('kew');
var fs=require('fs-extra');
var config = new (require('v-conf'))();
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
var spawn = require('child_process').spawn;
var json = require('json');
var stringify = require('json-stringify');

module.exports = lcdcontroller;
function lcdcontroller(context) {
	var self = this;

	this.context = context;
	this.commandRouter = this.context.coreCommand;
	this.logger = this.context.logger;
	this.configManager = this.context.configManager;

}

// Tell Volumio that the settings are saved in a file called config.json
lcdcontroller.prototype.getConfigurationFiles = function()
{
	return ['config.json'];
}

lcdcontroller.prototype.onVolumioStart = function()
{
	var self = this;
	var configFile=this.commandRouter.pluginManager.getConfigurationFile(this.context,'config.json');
	this.config = new (require('v-conf'))();
	this.config.loadFile(configFile);

    return libQ.resolve();
}

// Tell Volumio what to do when the plugin gets enabled
lcdcontroller.prototype.onStart = function() {
    var self = this;
    var defer=libQ.defer();

    spawn('/usr/bin/killall', ['python'], {
    		detached: true
    });
    // Wait some time for '/usr/bin/killall' to complete
    var waitTimestamp = new Date(new Date().getTime() + 2000);
    while(waitTimestamp > new Date()){};
 
    spawn('/usr/bin/python', ['/data/plugins/user_interface/lcdcontroller/LCDcontroller/main.py'], {
      detached: true
    });

    //  Once the Plugin has successfull started resolve the promise
    defer.resolve();

    return defer.promise;
};

// Tell Volumio what to do when the plugin gets disabled
lcdcontroller.prototype.onStop = function() {
    var self = this;
    var defer=libQ.defer();
    // Use spawn with option 'detached: true' to run a command. 'detached: false' will crash Volumio instantly, because 'child process /usr/bin/killall' exited.
    spawn('/usr/bin/killall', ['python'], {
    		detached: true
    });
    // Once the Plugin has successfull stopped resolve the promise
    defer.resolve();

    return libQ.resolve();
};

lcdcontroller.prototype.onRestart = function() {
    var self = this;
    // Use this if you need it
};


function restartLCD() {
    spawn('/usr/bin/killall', ['python'], {
    	detached: true
    });
    // Wait some time for '/usr/bin/killall' to complete
    var waitTimestamp = new Date(new Date().getTime() + 450);
    while(waitTimestamp > new Date()){};

    spawn('/usr/bin/python', ['/data/plugins/user_interface/lcdcontroller/LCDcontroller/main.py'], {
    	detached: true
    });
}

restartLCD();


// Configuration Methods -----------------------------------------------------------------------------

// Load the settings and display them in the "settings"-page
lcdcontroller.prototype.getUIConfig = function() {
    var defer = libQ.defer();
	var self = this;

	var lang_code = this.commandRouter.sharedVars.get('language_code');

	self.commandRouter.i18nJson(__dirname+'/i18n/strings_'+lang_code+'.json',
		__dirname+'/i18n/strings_en.json',
		__dirname + '/UIConfig.json')
		.then(function(uiconf)
		{
			// Load everything from config.json into the UIconfig
			// Example: uiconf.sections[0].content[0].value = self.config.get('<setting_name>');    // Where <setting_name> is the name of the setting stored in config.json

			// Load config_text_split_string into UIconfig
			uiconf.sections[0].content[0].value = self.config.get('config_text_split_string');
			// Load config_welcome_message_bool into UIconfig
			uiconf.sections[0].content[1].value = self.config.get('config_welcome_message_bool');
			// // Load config_welcome_message_duration into UIconfig
			uiconf.sections[0].content[2].value = self.config.get('config_welcome_message_duration');
			// // Load config_welcome_message_string_one into UIconfig
			uiconf.sections[0].content[3].value = self.config.get('config_welcome_message_string_one');
			// // Load config_welcome_message_string_two into UIconfig
			uiconf.sections[0].content[4].value = self.config.get('config_welcome_message_string_two');
			// Load config_welcome_message_string_three into UIconfig
			uiconf.sections[0].content[5].value = self.config.get('config_welcome_message_string_three');
			// Load config_welcome_message_string_four into UIconfig
			uiconf.sections[0].content[6].value = self.config.get('config_welcome_message_string_four');
			// Load config_lcd_address into UIconfig
			uiconf.sections[0].content[7].value = self.config.get('config_lcd_address');
			// Load config_weather_forecast_bool into UIconfig
			uiconf.sections[0].content[8].value = self.config.get('config_weather_forecast_bool');
			// Tell Volumio everything went very well
			defer.resolve(uiconf);
		})
		.fail(function()
		{
			// Something went wrong. Tell the user about it and abort loading the settings-page.
			self.commandRouter.pushToastMessage('error', "LCDcontroller", "Error: Could not load settings");
			defer.reject(new Error());
		});

	return defer.promise;
};

// Function to save the settings the user wants to have
lcdcontroller.prototype.saveUIConfig = function(data) {
   var defer = libQ.defer();
   var self = this;
   // For every setting, save it's value to config.json
   // Example: self.config.set('<setting_name>', data['<UIconfig_value>']);   // Where <setting_name> is stored in config.json and <UIconfig_value> retreived from the UIconfig.

   // Save text_split_string's value in config_text_split_string in config.json
   self.config.set('config_text_split_string', data['text_split_string']);
   // Save welcome_message_bool's value in config_welcome_message_bool in config.json
   self.config.set('config_welcome_message_bool', data['welcome_message_bool']);
   // Save welcome_message_duration's value in config_welcome_message_duration in config.json
   self.config.set('config_welcome_message_duration', data['welcome_message_duration']);
   // Save welcome_message_string_one's value in config_welcome_message_string_one in config.json
   self.config.set('config_welcome_message_string_one', data['welcome_message_string_one']);
   // Save welcome_message_string_two's value in config_welcome_message_string_two in config.json
   self.config.set('config_welcome_message_string_two', data['welcome_message_string_two']);
   // Save welcome_message_string_three's value in config_welcome_message_string_three in config.json
   self.config.set('config_welcome_message_string_three', data['welcome_message_string_three']);
   // Save welcome_message_string_four's value in config_welcome_message_string_four in config.json
   self.config.set('config_welcome_message_string_four', data['welcome_message_string_four']);
   // Save lcd_address's value in config_lcd_address in config.json
   self.config.set('config_lcd_address', data['lcd_address']);
   // Save config_weather_forecast_bool's value in config_weather_forecast_bool in config.json
   self.config.set('config_weather_forecast_bool', data['weather_forecast_bool']);

   // After saving all settings, restart the LCDcontroller
   var waitTimestamp = new Date(new Date().getTime() + 4000);
   while(waitTimestamp > new Date()){};
   restartLCD();

   // Tell Volumio everything went fine
   return defer.promise;
};

lcdcontroller.prototype.setUIConfig = function(data) {
	var self = this;
	//Perform your installation tasks here
};

lcdcontroller.prototype.getConf = function(varName) {
	var self = this;
	return ['config.json'];
};

lcdcontroller.prototype.setConf = function(varName, varValue) {
	var self = this;
};
