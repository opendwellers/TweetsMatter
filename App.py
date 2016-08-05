from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import sys
import simplejson as json
import configparser as ConfigParser
import urllib3

class listener(StreamListener):
    def __init__(self, target):
        self.target = target

    def on_data(self, data):
        # Load the json data
        data = json.loads(data)

        # Get the bot owner's information
        user = data.get('user')

        # Get the user name and the message of the tweet
        name = user.get('screen_name')
        message = data.get('text')

        # Make sure the tweeter is the one we want
        if name != self.target.screen_name:
            return True

        # Send the payload to the mattermost server
        payload = json.dumps(self.create_payload(message))
        http.request('POST', hook, headers={'Content-Type':'application/json'}, body=payload)

        return True

    def on_error(self, status):
        print(status)

    def create_payload(self, message):
        screen = self.target.screen_name

        name = self.target.name
        icon = 'http://icons.iconarchive.com/icons/sicons/basic-round-social/512/twitter-icon.png'
        profile = '@' + screen
        url = 'https://twitter.com/' + screen

        return {
            'username' : 'Trump',
            'icon_url' : avatar,

            'attachments' : [{
                'color'      : '#FF8000',
                'author_name': name,
                'author_icon': icon, 
                'title': profile,
                'title_link': url,
                'fields': [{
                    'short' : False,
                    'value' : message
                }]
            }]
        }

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

    # Get the user object
    api = API(auth)
    target = api.get_user('25073877')

    # Create Twitter stream
    twitterStream = Stream(auth, listener(target))
    twitterStream.filter(follow=['25073877'])
