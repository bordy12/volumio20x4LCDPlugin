from mpd import MPDClient

mpd_host = "127.0.0.1"
mpd_port = "6600" 
mpd_password = "volumio"

client = MPDClient()
client.connect(mpd_host, mpd_port)

currentSong = client.currentsong()
print(str(currentSong))
