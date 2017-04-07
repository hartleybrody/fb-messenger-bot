import os
from urlparse import urlparse

import redis

DEFAULT_EXPIRES = 4 * 60 * 60  # number of seconds before we auto-expire the conversation state


class RedisCache(object):
    """docstring for RedisCache"""
    def __init__(self):
        super(RedisCache, self).__init__()
        u = urlparse(os.environ["REDIS_URL"])
        self.redis = redis.StrictRedis(host=u.hostname, port=u.port, password=u.password, db=0)

    def set(self, k, v, expires=DEFAULT_EXPIRES):
        return self.redis.set(k, v, ex=int(expires))

    def get(self, k, default=None):
        return self.redis.get(k) or default

    def delete(self, k):
        return self.redis.delete(k)


# instantiate our cache so that we can simply
# import the name 'redis' and use it anywhere
redis = RedisCache()