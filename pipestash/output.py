# output module. only does redis for now
import urlparse

class Output(object):
    def __init__(self, redis_url, redis_key):
        url = urlparse.urlparse(redis_url)
        self.redis = StrictRedis(host=url.hostname, port = url.port, db=sub(r'^/','',url.path))
        self.redis_key = redis_key

    def do(self, item):
        self.redis.rpush(self.redis_key, item)
