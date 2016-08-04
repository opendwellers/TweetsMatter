from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import simplejson as json
import configparser as ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("conf/config")

c_key = Config.get('twitter','Ckey')
c_secret = Config.get('twitter','CSecret')
a_token = Config.get('twitter','AToken')
a_secret = Config.get('twitter','ASecret')

class listener(StreamListener):
    def on_data(self, data):
        data = json.loads(data)
        print(data.get("text")) 
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(follow=['760836832699359233'])
