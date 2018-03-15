#!/bin/bash

echo "Install lcdcontroller Dependencies"
echo "    Executing sudo apt-get update"
# TODO: UNCOMMENT THIS!
# sudo apt-get update
echo "    Executing: sudo apt-get sudo apt-get -y install python-mpd python-smbus"
# TODO: UNCOMMENT THIS!
# sudo apt-get -y install python-mpd python-smbus

echo "Making LCD-controller python-script executable"
echo "    Executing: sudo chmod +x /data/plugins/user_interface/lcdcontroller/LCDcontroller/scrollText.py"
sudo chmod +x /data/plugins/user_interface/lcdcontroller/LCDcontroller/scrollText.py

echo "If the plugin does not turn on after installing, restart Volumio"
echo "plugininstallend"
