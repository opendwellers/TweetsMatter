FROM frolvlad/alpine-python3:latest
MAINTAINER Gabriel G. <gabrielpolloguilbert@gmail.com>

ADD App.py .
ADD conf/template .

RUN pip install tweepy simplejson urllib3

ENTRYPOINT ["python3", "App.py", "template"]
