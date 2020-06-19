# Welcome

Welcome to the project page for a plugin I created for Volumio2 for the Raspberry Pi, actually I'm running it on a Pi 2.
This project belongs to the one created by Tom Niesse, I rewrote the main python procedure, it now uses a slightly different I2C driver I need to manage my custom characters set.
It can retreive information about songs and webradio's and print them on an LCD-screen with I2C (4x20).<br>Pictures of the 4x20 LCD:<br>

I fitted the Pi2 into an ex-FM radio case i have found somewhere in my house, this is the result:
<img width="380px" src='https://user-images.githubusercontent.com/20586835/85121964-16d85880-b226-11ea-9532-93dd40dd7e59.jpg' alt='MyRadio_01'><br>
<img width="380px" src='https://user-images.githubusercontent.com/20586835/85121980-2061c080-b226-11ea-9343-be43a803f042.jpg' alt="MyRadio_02">

Note: The buttons on the top are still functional! I can shut down the Pi, pause/play the song, increase/decrease volume or select the next/previous song.

## Plugin features

The plugin can display information about music files and webradio's when they are playing, such as:
  - Displaying the name of the radio station the webradio is playing
  - Displaying the name of the song that the webradio is playing
  - Displaying music files, either the embedded tags or the filename
  - Displaying elapsed time for music files
  - Displaying a pause icon next to the elapsed time for music files if the music is paused at any time
  - Separating 'title - artist-name - album-name' into<br>title<br>artist-name<br>album-name<br>for webradios and music files
  - Displaying a welcome-message at startup
  - Displaying volume % when it changes
  - Displaying weather forecast (edit the main.py to meets your needs first!)

The plugin can auto-update information when it changes, for exmaple, switching from webradio to a music file, pausing music files, etc.

## How to install the plugin

It seems that Volumio does not do file-upload anymore, as told here:
https://volumio.org/forum/way-upload-unofficial-plugin-t9155.html.
I will look for a fitting solution to this.

## How to uninstall the plugin
The plugin can be uninstalled as any other Volumio plugin:
- Go to the installed plugins and click "Uninstall"

After uninstalling, the LCD might still show some text and it will look like it froze.<br>I will fix this in the future.

## Change plugin settings

The settings can be changed in the plugin's settings page. In Volumio: Go to the plugin manager, turn the plugin on if it is currently turned off and click "Settings".

## Turning the plugin on and off

This can also be done via the plugin-menu. After turning the plugin off, some text can still be displayed on the LCD-screen. I will fix this in the future
