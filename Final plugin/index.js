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

// "Volumio needs this function" ~ The "how write a plugin" guide
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

lcdcontroller.prototype.onStart = function() {
    var self = this;
    var defer=libQ.defer();

    //Start a detached process, without those parent-child-relationships. This way, someone can turn the plugin on and off without destroying the index.js process
    spawn('/data/plugins/user_interface/lcdcontroller/LCDcontroller/scrollText.py', ['TODO_insert_any_arguments_here_later_please'], {
    	detached: true
    }); 
    // Tell the user the plugin started
    self.commandRouter.pushToastMessage('info', "LCDcontroller", "Plugin started");

    //  Once the Plugin has successfull started resolve the promise
    defer.resolve();

    return defer.promise;
};

lcdcontroller.prototype.onStop = function() {
    var self = this;
    var defer=libQ.defer();
    spawn('/usr/bin/killall', ['python'], {
    		detached: true
    });
    // Tell the user the plugin stopped
    self.commandRouter.pushToastMessage('info', "LCDcontroller", "Plugin stopped");
    // Once the Plugin has successfull stopped resolve the promise
    defer.resolve();

    return libQ.resolve();
};

lcdcontroller.prototype.onRestart = function() {
    var self = this;
    // Optional, use if you need it
};


// Configuration Methods -----------------------------------------------------------------------------

lcdcontroller.prototype.getUIConfig = function() {
    var defer = libQ.defer();
	var self = this;

	var lang_code = this.commandRouter.sharedVars.get('language_code');

	self.commandRouter.i18nJson(__dirname+'/i18n/strings_'+lang_code+'.json',
		__dirname+'/i18n/strings_en.json',
		__dirname + '/UIConfig.json')
		.then(function(uiconf)
		{
			//uiconf.sections[0].content[0].value.value = configContents['config_text_split_string']['value'];
			self.commandRouter.pushToastMessage('info', "LCDcontroller", "UIconf loaded");
			defer.resolve(uiconf);
		})
		.fail(function()
		{
			defer.reject(new Error());
		});

	return defer.promise;
};

lcdcontroller.prototype.saveUIConfig = function(data) {
   var defer = libQ.defer();
   var self = this;
   self.config.set('config_text_split_string', data['text_split_string']);
   self.config.set('config_welcome_message_bool', data['welcome_message_bool']);
   self.config.set('config_welcome_message_duration', data['welcome_message_duration']);
   self.config.set('config_welcome_message_string_one', data['welcome_message_string_one']);
   self.config.set('config_welcome_message_string_two', data['welcome_message_string_two']);
   self.config.set('config_welcome_message_string_three', data['welcome_message_string_three']);
   self.config.set('config_welcome_message_string_four', data['welcome_message_string_four']);
   self.config.set('config_host', data['host']);
   self.config.set('config_lcd_address', data['lcd_address']);
   self.commandRouter.pushToastMessage('info', "LCDcontroller", "Settings have been saved");
   return defer.promise;
};

lcdcontroller.prototype.setUIConfig = function(data) {
	var self = this;
	//Perform your installation tasks here
};

lcdcontroller.prototype.getConf = function(varName) {
	var self = this;
	return ['config.json']
};

lcdcontroller.prototype.setConf = function(varName, varValue) {
	var self = this;
};
