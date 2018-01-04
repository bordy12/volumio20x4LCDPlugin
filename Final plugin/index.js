'use strict';

var libQ = require('kew');
var fs=require('fs-extra');
var config = new (require('v-conf'))();
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
var spawn = require('child_process').spawn;


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

// TODO: Test which of these 2 functions actually load config.json properly (For now I'll include 2 functions, since it doesn't affect the plugin too much)
lcdcontroller.prototype.getConfigurationFile = function()
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

	//Start a detached process, without those parent-child-relationships. This way someone can turn the plugin on and off without destroying the index.js process
	spawn('/data/plugins/user_interface/lcdcontroller/LCDcontroller/scrollText.py', ['TODO_insert_any_arguments_here_later_please'], {
    		detached: true
	});

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
	    // Make sure the configuration from config.json gets loaded into UIconfig values
            // Load text_split_string from config.json into UIconfig
            uiconf.sections[0].content[0].value = self.config.get('text_split_string');
            // Load welcome_message_bool from config.json into UIconfig
	    uiconf.sections[0].content[1].value = self.config.get('password');
            // Load welcome_message_duration from config.json into UIconfig
            uiconf.sections[0].content[2].value = self.config.get('bitrate');
            // Load welcome_message_string_one from config.json into UIconfig
            // Load welcome_message_string_two from config.json into UIconfig
	    // Load welcome_message_string_three from config.json into UIconfig
            // Load welcome_message_string_four from config.json into UIconfig
            // Load host from config.json into UIconfig
            defer.resolve(uiconf);
        })
        .fail(function()
        {
            defer.reject(new Error());
        });

    return defer.promise;
};

lcdcontroller.prototype.saveConfig = function() {
	var self = this;

        var defer = libQ.defer();
	//Save config here please
	defer.resolve({});

        return defer.promise;
}

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
	//TODO: Save configs to config.json
};
