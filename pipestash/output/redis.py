import urlparse
import pipestash.output

class RedisOutput(pipestash.output.Output):
    def __init__(self, config):
        redis_url = urlparse.urlparse(config.redis_url)
        self.redis = StrictRedis(host=redis_url.hostname, port = redis_url.port, db=sub(r'^/','',redis_url.path))
        self.redis_key = config.redis_key

    def do(self, item):
        self.redis.rpush(self.redis_key, item)
