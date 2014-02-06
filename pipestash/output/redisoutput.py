import urlparse
import pipestash.output
import redis
import json
import inspect
import re
import time
import random

class RedisOutput(pipestash.output.Output):
    def __init__(self, config):
        redis_url = urlparse.urlparse(config.redis_url)
        self.redis = redis.StrictRedis(host=redis_url.hostname, port = redis_url.port, db=re.sub(r'^/','',redis_url.path))
        self.redis_key = config.redis_key

    def do(self, item):
        while True:
            try:
                self.redis.rpush(self.redis_key, item)
                break
            except (redis.ConnectionError, redis.ResponseError):
                time.sleep(config.timeout * random.random())
                pass
