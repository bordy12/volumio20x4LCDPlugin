echo "Welcome to the plugin builder for Volumio LCD controller!"
echo "Before the build of this plugin starts, I need a few info's."
echo " "

read -p "MPDHOST: " MPDHOST

echo "Applying configuration "
# Create custom scrollText.py

echo "Creating plugin "
# Create plugin by zipping all the files in the plugin folder

echo " "
echo "Volumio plugin has been created!"
echo "It's been stored here:	`pwd ~`/plugin.zip "
