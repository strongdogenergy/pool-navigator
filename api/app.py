import time
import redis
from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_secure_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('secure_hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
@cross_origin()
def hello():
    count = get_hit_count()
    return {
        "hits": count,
    }

@app.route('/secure')
@cross_origin()
def getSecureHits():
    count = get_hit_count()
    secure_count = get_secure_hit_count()
    return {
        "hits": count,
        "secure_hits": secure_count,
    }