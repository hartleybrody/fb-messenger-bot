import os
import redis

class Kova:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))
        self.redis.set('test', 'test is success')

    def chat(self, input, userid):
        if userid not in self.redis:
            self.redis.set(userid, 0)
        chapter = self.redis.get(userid)
        chatper += 1
        self.redis.set(userid, chapter)
        return 'you messaged + ' + chapter + ' times'
