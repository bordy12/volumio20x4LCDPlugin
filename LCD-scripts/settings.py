# What text must the display show at boot? (Default: 'Welcome!' on the second line)
def getWelcomeMessage():
        welcome_message = {
                "Line1": " ",
                "Line2": "Welcome!",
                "Line3": " ",
                "Line4": " "
                }
        return welcome_message
# How long should the welcome-message stay?
def getWelcomeMessageDuration():
        welcomeMessageDuration = 2
        return welcomeMessageDuration

# How often should the script check for new song/webradio info?
def getInfoRefreshInterval():
        infoRefreshInterval = 0.5
        return infoRefreshInterval
        
# Where should the script get it's information from?
def getHostIP():
	volumioHost = '127.0.0.1'  # This can be an IP address or 'localhost'
	return volumioHost
