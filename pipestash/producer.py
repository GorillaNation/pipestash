# read from stdin, put into queue
# also restart the consumer if it dies for some reason
import sys
import datetime


def produce(config, queue, create_consumer):
    consumer = create_consumer()

    while True:
        # read the line
        line = sys.stdin.readline()
        if not line:
            # EOF
            break
        # strip trailing newline
        line = line.rstrip()

        if config.stdout:
            print line

        # check the consumer and restart if necessary
        if not consumer.is_alive():
            consumer.join()
            consumer = create_consumer()

        # toss it in the queue
        queue.put([datetime.datetime.utcnow().isoformat('T') + 'Z', line])
    queue.put(None)
    queue.close()
    return consumer
