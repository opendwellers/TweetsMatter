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
        # Load the json data
        data = json.loads(data)

        # Get the bot owner's information
        user = data.get('user')

        # Get the tweeter and the messagea
        tweeter = user.get('screen_name')
        message = data.get('text')

        # Make sure the tweeter is the one we want
        if tweeter != 'realDonaldTrump':
            return True

        # Send the payload to the mattermost server
        payload = json.dumps(self.create_payload("asdasd"))
        http.request('POST', hook, headers={'Content-Type':'application/json'}, body=payload)

        return True

    def on_error(self, status):
        print(status)

    def create_payload(self, message):
        return {
            'username' : 'Trump',
            'icon_url' : avatar,

            'attachments' : [{
                'fallback'   : 'test',
                'color'      : '#FF8000',
                'author_name': 'Donald Trump',
                'author_icon': 'http://icons.iconarchive.com/icons/sicons/basic-round-social/512/twitter-icon.png', 
                'title': '@realdonaldtrump',
                'title_link': 'https://twitter.com/realdonaldtrump',
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

    # Create Twitter stream
    twitterStream = Stream(auth, listener())
    twitterStream.filter(follow=['25073877'])
