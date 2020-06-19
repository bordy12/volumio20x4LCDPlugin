# Welcome

Welcome to the project page for a plugin I created for Volumio2 for the Raspberry Pi, actually I'm running it on a Pi 2.
This project belongs to the one created by Tom Niesse, I rewrote the main python procedure, it now uses a slightly different I2C driver I need to manage my custom characters set.
It can retreive information about songs and webradio's and print them on an LCD-screen with I2C (4x20).
Addionatly it can show weather forecast infos, in this case you need to edit the python script to work with your favourite weather forecast service.

I fitted the Pi2 and the LCD into an FM radio case i have found somewhere in my house, this is the result:
<img width="380px" src='https://user-images.githubusercontent.com/20586835/85121964-16d85880-b226-11ea-9532-93dd40dd7e59.jpg' alt='MyRadio_01'><br>
<img width="380px" src='https://user-images.githubusercontent.com/20586835/85121980-2061c080-b226-11ea-9343-be43a803f042.jpg' alt="MyRadio_02">

Note: The buttons on the top are still functional! I can shut down the Pi, pause/play the song, increase/decrease volume or select the next/previous song. To achieve this I installed a plugin named "GPIO Buttons".

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
  - Displaying weather forecast infos from XML weather service https://www.arpa.veneto.it/

The plugin can auto-update information when it changes, for exmaple, switching from webradio to a music file, pausing music files, etc.
Weather forecast XML file has to be downloaded in the home dir with an external script and optionally scheduled with cron.

## How to install the plugin

Clone and extract the archive onto a new directory of your Pi's home (eg. /home/volumio/lcdcontroller)
Then type: 
cd /home/volumio/lcdcontroller
volumio plugin install

## How to uninstall the plugin

The plugin can be uninstalled as any other Volumio plugin:
- Go to the installed plugins and click "Uninstall"

After uninstalling, the LCD might still show some text and it will look like it froze.

## Change plugin settings

The settings can be changed in the plugin's settings page. In Volumio: Go to the plugin manager, turn the plugin on if it is currently turned off and click "Settings".

## Turning the plugin on and off

This can also be done via the plugin-menu. After turning the plugin off, some text can still be displayed on the LCD-screen.
