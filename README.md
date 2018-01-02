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
  - Separating '01 - title - artist' into<br>01<br>title<br>artist<br>for webradios and music files
  - Displaying a welcome-message at startup (see "Change plugin settings" on how to customize this)

The plugin can auto-update information when it changes, for exmaple, switching from webradio to a music file, pausing music files, etc.

## How to install the plugin
- Go to http://your_volumio_name.local (or http://your_volumio_ip/ if the first option does not work)
- Click the gears-icon in the top-right
- Click "PLUGINS"
- Click "Upload Plugin"
- Upload plugin.zip
- After the plugin has been successfully installed, reboot volumio<br>Optional (will be automated in the future): You can SSH into volumio and run 'sudo /etc/init.d/volumioLCDservice start' instead of rebooting

## How to uninstall the plugin
The plugin can be uninstalled as any other Volumio plugin:
- Go to the installed plugins and click "Uninstall"

After uninstalling, the LCD might still show some text and it will look like it froze.<br>I will fix this in the future. It is nothing to worry about though.

## Change plugin settings

The plugin settings cannot be changed via the plugin-settings yet.<br>However, after installing the plugin, you can SSH into Volumio and change '/opt/LCDcontroller/settings.py' to tweak some settings, for example the welcome-message.<br>I will add plugin settings later.

## Turning the plugin on and off

This plugin cannot be turned on or off via the plugin-settings yet. The plugin stays enabled until it is uninstalled.<br>I will add this feature in the future.
