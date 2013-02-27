# read from stdin, put into queue
# also restart the consumer if it dies for some reason
import sys
import datetime
import signal


def produce(config, queue, create_consumer):
    consumer = create_consumer()

    try:
        def graceful(signum, frame):
            raise Exception("caught {0} signal, exiting".format(signum))

        signal.signal(signal.SIGTERM, graceful)
        signal.signal(signal.SIGINT, graceful)
        signal.signal(signal.SIGQUIT, graceful)

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
    except Exception as e:
        print "caught exception {0}, queue length ~{1}".format(e, queue.qsize())
        # FIXME: handle this properly. maybe by putting a message in the queue
        # if there's an uncaught exception besides an interrupt?
        pass
    queue.put(None)
    queue.close()
    return consumer
