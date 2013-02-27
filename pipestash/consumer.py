# this function is the top level of the execution of the
# child process. I think that's how I'm gonna do it at least.

import json

def consume(queue, output, config):
    event = {
        "@fields": config.fields,
        "@type": config.type,
        "@tags": config.tags,
        "@source_host": config.source_path,
        "@source_path": config.source_host,
        "@source": config.source
    }

    for item in iter(queue.get, None):
        event["@timestamp"] = item[0]
        event["@message"] = item[1]
        try:
            output.do(json.dumps(event))
        except:
            # FIXME: do something about exceptions
            pass
