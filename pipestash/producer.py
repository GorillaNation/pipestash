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

        print "LINE: line"

        event["@timestamp"] = datetime.datetime.utcnow().isoformat('T') + 'Z'
        line = line.rstrip()
        event["@message"] = line

        if not consumer.is_alive():
            print "consumer is dead, long live consumer!"
            consumer.join()
            consumer = create_consumer()

        print "putting shit in queue"
        str = json.dumps(event)
        #queue.put(json.dumps(event))
    queue.close()
