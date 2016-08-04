from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import simplejson as json
import configparser as ConfigParser
import urllib3

Config = ConfigParser.ConfigParser()
Config.read("conf/config")

c_key = Config.get('twitter','Ckey')
c_secret = Config.get('twitter','CSecret')
a_token = Config.get('twitter','AToken')
a_secret = Config.get('twitter','ASecret')
hook = Config.get('mattermost','Hook')
avatar = 'http://i.imgur.com/RCKRF2B.png'

http = urllib3.PoolManager()

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

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(follow=['25073877'])
