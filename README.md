# Welcome

Welcome to the project page for a plugin I created for Volumio2 for the Raspberry Pi 3.
It can retreive information about songs and webradio's and print them on an LCD-screen with I2C (4x20).<br>Pictures of the 4x20 LCD:<br>
<img width="380px" src='https://www.raspberrypi-spy.co.uk/wp-content/uploads/2015/04/i2c_backpack_02-1024x597.jpg' alt='LCD_back'><br>
<img width="380px" src='http://domoticx.com/wp-content/uploads/YM2004A-LCD-Display-2x20-4x20.jpg' alt="LCD_front">

## Plugin features

The plugin can display information about music files and webradio's when they are playing, such as:
  - Displaying the name of the radio station the webradio is playing
  - Displaying the name of the song that the webradio is playing
  - Displaying music files, either the embedded tags or the filename
  - Displaying elapsed time for music files
  - Displaying a pause icon next to the elapsed time for music files if the music is paused at any time
  - Separating 'title - artist-name - album-name' into<br>title<br>artist-name<br>album-name<br>for webradios and music files
  - Displaying a welcome-message at startup

The plugin can auto-update information when it changes, for exmaple, switching from webradio to a music file, pausing music files, etc.

## How to install the plugin

It seems that Volumio does not do file-upload anymore, as told here:
https://volumio.org/forum/way-upload-unofficial-plugin-t9155.html
I will look for a fitting solution to this.

### How to bundle the plugin myself?
- Download all the files from this GitHub-page
- In your file-manager, go into the "plugin"-folder (this folder contains the source code)
- Select all the files in this folder and put them in a zip-file (the name of the zip-file does not matter)
- If another version of this plugin is already installed on Volumio, remove it.
- Upload the <pluginname>.zip you just created to Volumio

## How to uninstall the plugin
The plugin can be uninstalled as any other Volumio plugin:
- Go to the installed plugins and click "Uninstall"

After uninstalling, the LCD might still show some text and it will look like it froze.<br>I will fix this in the future.

## Change plugin settings

The settings can be changed in the plugin's settings page. In Volumio: Go to the plugin manager, turn the plugin on if it is currently turned off and click "Settings".

## Turning the plugin on and off

This can also be done via the plugin-menu. After turning the plugin off, some text can still be displayed on the LCD-screen. I will fix this in the future
