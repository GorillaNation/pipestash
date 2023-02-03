# output module. only does redis for now
import urllib.parse

class Output(object):
    def __init__(self, config):
        raise Exception("subclasses need to override this method")

    def do(self, item):
        raise Exception("subclasses need to override this method")

