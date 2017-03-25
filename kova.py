import os
import redis
import pickle

class Kova:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))

    def chat(self, input, user_id):
        self.redis.hsetnx('users', user_id + 'chapter', int(0))
        chapter = int(self.redis.hget('users', user_id + 'chapter'))
        chapter += 1
        self.redis.hset('users', userid + 'chapter', int(chapter))
        return 'you messaged + ' + chapter + ' times'
