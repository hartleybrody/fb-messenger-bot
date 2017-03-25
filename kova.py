import os
import redis

class Kova:

    def __init__(self):

    def chat(self, input, userinfo):
        chapter = userinfo['chapter']
        chapter += 1
        redis.set(userid, chapter)
        return 'you messaged + ' + chapter + ' times'
