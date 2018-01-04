#!/bin/bash

echo "Install lcdcontroller Dependencies"
echo "    Executing sudo apt-get update"
#sudo apt-get update
echo "    Executing: sudo apt-get sudo apt-get -y install python-mpd python-smbus"
#sudo apt-get -y install python-mpd python-smbus

echo "Making LCD-controller python-script executable"
echo "    Executing: sudo chmod +x /data/plugins/user_interface/lcdcontroller/LCDcontroller/scrollText.py"
sudo chmod +x /data/plugins/user_interface/lcdcontroller/LCDcontroller/scrollText.py

echo "If the settings are not visible after installing the plugin and clicking settings, a restart should fix it."
echo "plugininstallend"
