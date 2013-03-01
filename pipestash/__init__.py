import socket
import argparse

def parseargs():
    # parse command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', required=True, help='the event type (required)')
    parser.add_argument('-r','--redis-url', help="specify the URL of the redis database to use, defaults to redis://localhost:6379/0", default='redis://localhost:6379/0')
    parser.add_argument('-R', '--redis-key', help="redis key to add events to, defaults to logstash", default='logstash')
    parser.add_argument('-T','--tags', action='append', nargs='*', help="tags to add to the event", default=[])
    parser.add_argument('-f', '--fields', nargs='*', metavar='field=value', action='append', help="fields to add to the event, FIELD=VALUE, separated by spaces", default=[])
    parser.add_argument('-s', '--source-path', help="specify the @source_path field, defaults to 'stdin'", default='stdin')
    parser.add_argument('-S', '--source-host', help="specify the @source_host field, defaults to the machine's FQDN", default=socket.getfqdn())
    parser.add_argument('-O', '--stdout', help="print read lines to stdout as well as to redis", action="store_true")
    parser.add_argument('-v', '--verbose', help="enable verbose mode", action="store_true")
    parser.add_argument('-q', '--queue-size', help="set the maximum size for the internal queue in number of messages, defaults to 10000", default=10000, type = int)
    parser.add_argument('-B', '--block', help="block reads if the queue is full. defaults to False", default=False, action='store_true')
    args = parser.parse_args()

    # set source
    args.source = "file:///{0}/{1}".format(args.source_host, args.source_path)

    # parse out fields
    fields = {}
    for fieldargs in args.fields:
        for fullfield in fieldargs:
            a,_,b = fullfield.partition("=")
            fields[a] = b
    args.fields = fields

    # flatten tags array
    tags = []
    for tagargs in args.tags:
        for tag in tagargs:
            tags.append(tag)
    args.tags = tags

    # verbose output
    if args.verbose:
        def verbose(s):
            print >> sys.stderr, s
    else:
        def verbose(s):
            pass

    return args
