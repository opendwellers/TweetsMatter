from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

c_key = "EjGa9Qarey1v5Q9NFiayO8ikN"
c_secret = "RbGIUEZhdHwId1GB01K8T0fTPnwah0Pc0q3RcxKIETq8dMnGfh"
a_token = "760836832699359233-oJv1BuImm2HqR5zHfA9klh415lMG3sq"
a_secret = "Llh4zbFuUj6fNfPb3QsuFFSr9oC0Bq51z0paKTndIehlM"

print("Authenticated with cosumer key : "+c_key+" and consumer secret :  "+c_secret)

class listener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["car"])
