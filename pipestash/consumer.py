# this function is the top level of the execution of the
# child process. I think that's how I'm gonna do it at least.

import json
import threading

class Consumer(threading.Thread):
    def __init__(self, queue, output, config):
        threading.Thread.__init__(self)
        self.queue = queue
        self.output = output
        self.event = {
            "@fields": config.fields,
            "@type": config.type,
            "@tags": config.tags,
            "@source_host": config.source_host,
            "@source_path": config.source_path,
            "@source": config.source
        }

    def run(self):
        for item in iter(self.queue.get, None):
            self.event["@timestamp"] = item[0]
            self.event["@message"] = item[1]
            try:
                self.output.do(json.dumps(self.event))
            except Exception as e:
                # FIXME: do something about exceptions
                pass
            self.queue.task_done()
        self.queue.task_done()
