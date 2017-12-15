'use strict';

var libQ = require('kew');
var fs=require('fs-extra');
var config = new (require('v-conf'))();
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;


module.exports = ControllerLCDcontroller;
function ControllerLCDcontroller(context) {
	var self = this;

	this.context = context;
	this.commandRouter = this.context.coreCommand;
	this.logger = this.context.logger;
	this.configManager = this.context.configManager;

}



ControllerLCDcontroller.prototype.onVolumioStart = function()
{
	var self = this;
	var configFile=this.commandRouter.pluginManager.getConfigurationFile(this.context,'config.json');
	this.config = new (require('v-conf'))();
	this.config.loadFile(configFile);

    return libQ.resolve();
}

ControllerLCDcontroller.prototype.onStart = function() {
    var self = this;
	var defer=libQ.defer();

	self.commandRouter.pushToastMessage('error', 'LCD Controller', 'Starting LCD controller');
	exec('/usr/bin/sudo /usr/bin/env python /home/volumio/LCDcontroller/scrollText.py &');
	// Once the Plugin has successfull started resolve the promise
	defer.resolve();

    return defer.promise;
};

ControllerLCDcontroller.prototype.onStop = function() {
    var self = this;
    var defer=libQ.defer();
    
    exec('/usr/bin/sudo /usr/bin/killall python &');
    // Once the Plugin has successfull stopped resolve the promise
    defer.resolve();

    return libQ.resolve();
};

ControllerLCDcontroller.prototype.onRestart = function() {
    var self = this;
    // Optional, use if you need it
};


// Configuration Methods -----------------------------------------------------------------------------

ControllerLCDcontroller.prototype.getUIConfig = function() {
    var defer = libQ.defer();
    var self = this;

    var lang_code = this.commandRouter.sharedVars.get('language_code');

    self.commandRouter.i18nJson(__dirname+'/i18n/strings_'+lang_code+'.json',
        __dirname+'/i18n/strings_en.json',
        __dirname + '/UIConfig.json')
        .then(function(uiconf)
        {


            defer.resolve(uiconf);
        })
        .fail(function()
        {
            defer.reject(new Error());
        });

    return defer.promise;
};


ControllerLCDcontroller.prototype.setUIConfig = function(data) {
	var self = this;
	//Perform your installation tasks here
};

ControllerLCDcontroller.prototype.getConf = function(varName) {
	var self = this;
	//Perform your installation tasks here
};

ControllerLCDcontroller.prototype.setConf = function(varName, varValue) {
	var self = this;
	//Perform your installation tasks here
};
