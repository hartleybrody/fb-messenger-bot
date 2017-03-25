import os
import redis

class Kova:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))
        self.redis.set('test', 'test is success')

    def chat(self, input, userid):
        if userid not in self.redis:
            userinfo = {'count': 0}
            self.redis.set(str(userid), userinfo)
        return 'you messaged + ' + self.redis.get(str(userid))['count'] + ' times'
