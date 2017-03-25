import os
import redis

class Kova:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))
        self.redis.set('test', 'test is success')

    def chat(self, input):
        self.chapter += 1
        return self.redis.get('test')
