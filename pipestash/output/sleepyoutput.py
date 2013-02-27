# this is a dummy load. can be used for testing purposes
# configure it with config.sleepytime = X where X is how
# long you want it to sleep before returning.

import pipestash.output
import time

class SleepyOutput(pipestash.output.Output):
    def __init__(self, config):
       self.sleepytime = config.sleepytime

    def do(self, item):
        time.sleep(self.sleepytime)
