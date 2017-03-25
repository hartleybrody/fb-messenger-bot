import os
import redis
import cPickle

class Kova:

    def __init__(self):
        self.redis = redis.from_url(os.environ.get("REDISCLOUD_URL"))

    def chat(self, input, user_id):
        if input == 'redis flushall':
            self.redis.flushall()
        if user_id not in self.redis.keys(): # if user first time talking
            initUser(user_id)
        user_data = self.getData(user_id)
        user_data['count'] += 1
        self.setData(user_id, user_data)
        return 'you messaged ' + str(user_data['count']) + ' times'

    def initUser(self, user_id):
        user_data = {'count': 0}
        self.redis.set(user_id, cPickle.dumps(user_data))

    def getData(self, user_id):
        return cPickle.loads(self.redis.get(user_id))

    def setData(self, user_id, user_data):
        self.redis.set(user_id, cPickle.dumps(user_data))
