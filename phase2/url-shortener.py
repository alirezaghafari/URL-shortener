import requests
import json
import flask
import sys
import os
from redis import Redis
from datetime import timedelta
import socket 


port = int(os.environ['PORT'])
time_to_expire = int(os.environ['TIME_TO_EXPIRE'])
API_Endpoint = os.environ['API_ENDPOINT']
API_KEY = os.environ['API_KEY']
url = os.environ['URL']

redis = Redis(host='redis', port = 6379) 
APP = flask.Flask(__name__) # create the Flask app


@APP.route('/', methods=['GET'])   # route for the home page
def get_url():
    host_name = socket.gethostname()

    if redis.exists(url) and redis.ttl(url) > 0: # check if the key exists
        return {'long-url': url , 'short-url': redis.get(url).decode() , 'host_name': host_name, 'isCached':'true'} # return the value from the cache
    linkRequest = {
    "destination": url
    , "domain": { "fullName": "rebrand.ly" }
    }

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": API_KEY,
    }

    r = requests.post(API_Endpoint, 
        data = json.dumps(linkRequest),
        headers=requestHeaders)

    link = r.json()

    redis.setex(    # set the key to expire in 5 minutes
    link["destination"],   # key
    timedelta(minutes=time_to_expire),  # time to expire
    link["shortUrl"] # value
    )

    return {'long-url': link["destination"]  ,'short-url': link["shortUrl"], 'host_name': host_name, 'isCached':'false'} # return the json response

if __name__ == '__main__':
    APP.run(host='0.0.0.0' , port=port)


