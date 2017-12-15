#!/bin/bash

# Uninstall dependendencies
# apt-get remove -y

# Stop the service

sudo /etc/init.d/volumioLCDservice stop

# Remove /opt/LCDcontroller folder
sudo rm -rf /opt/LCDcontroller

# Disable LCDservice and remove it
sudo update-rc.d -f volumioLCDcontroller remove
sudo rm -rf /etc/init.d/volumioLCDcontroller

echo "Done"
echo "pluginuninstallend"
