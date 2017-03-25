import os
import redis
import cPickle

class Kova:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))

    def chat(self, input, user_id):
        if user_id not in self.redis.keys():
            userdata = {'count': 0}
            self.redis.set(user_id, cPickle.dumps(userdata))
        userdata = cPickle.load(self.redis.get(user_id))
        userdata['count'] += 1
        self.redis.set(user_id cPickle.dumps(userdata))
        return 'you messaged + ' + userdata['count'] + ' times'
