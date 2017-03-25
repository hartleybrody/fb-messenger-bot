import os
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import redis

class Kova:

    def __init__(self):
        self.redisurl = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
        self.redis = redis.Redis(host=url.hostname, port=url.port, password=url.password)
        self.redis.set('test', 'test is success')

    def chat(self, input):
        self.chapter += 1
        return self.redis.get('test')
