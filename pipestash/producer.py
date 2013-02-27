# read from stdin, put into queue
# also restart the consumer if it dies for some reason
import sys
import datetime
import json


def produce(config, queue, create_consumer):
    consumer = create_consumer()
    event = {
        "@fields": config.fields,
        "@type": config.type,
        "@tags": config.tags,
        "@source_host": config.source_host,
        "@source_path": config.source_path,
        "@source": config.source
    }

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        event["@timestamp"] = datetime.utcnow().isoformat('T') + 'Z'
        line = line.rstrip()
        event["@message"] = line

        if not consumer.is_alive():
            consumer.join()
            consumer = create_consumer()

        queue.put(json.dumps(event))
    queue.close()
