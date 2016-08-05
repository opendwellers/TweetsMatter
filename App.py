from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import sys
import simplejson as json
import configparser as ConfigParser
import urllib3

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        print(data)
        text = data.get('text')
        user = data.get('user')
        screen_name = user.get('screen_name')
        payload = {'username' : 'Trump', 'icon_url' : avatar, 'text' : data.get("text")}
        print(screen_name)
        if screen_name == 'realDonaldTrump':
            print("sending ... ")
            r = http.request('POST',hook ,headers={'Content-Type':'application/json'} ,body=json.dumps(payload))
            print(r.read())
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # Make sure the config file was given
    if (len(sys.argv) != 2):
        print("You must only specify the path to the configuration file.")
        exit(1)

    # Make sure the file path is valid
    path = sys.argv[1]
    if (not os.path.isfile(path)):
        print("The specified config file `" + path + "` doesn't exist.")
        exit(1)

    # Load the configuration file
    Config = ConfigParser.ConfigParser()
    Config.read(path)

    # Parse the configuration
    try:
        c_key = Config.get('twitter','Ckey')
        c_secret = Config.get('twitter','CSecret')
        a_token = Config.get('twitter','AToken')
        a_secret = Config.get('twitter','ASecret')
        avatar = Config.get('mattermost', "AvatarURL")
        hook = Config.get('mattermost','Hook')
    except ConfigParser.NoOptionError as exception:
        print(exception)
        exit(1)

    # Get an http manager
    http = urllib3.PoolManager()

    # Create Twitter OAuth tokens
    auth = OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token, a_secret)

    # Create Twitter stream
    twitterStream = Stream(auth, listener())
    twitterStream.filter(follow=['25073877'])
