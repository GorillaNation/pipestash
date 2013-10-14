import socket
import optparse

def parseargs():
    # parse command line
    parser = optparse.OptionParser()
    parser.add_option('-t', '--type', dest='type', help='the event type (required)')
    parser.add_option('-r','--redis-url', dest='redis_url', help="specify the URL of the redis database to use, defaults to redis://localhost:6379/0", default='redis://localhost:6379/0')
    parser.add_option('-R', '--redis-key', dest='redis_key', help="redis key to add events to, defaults to logstash", default='logstash')
    parser.add_option('-T','--tags', dest='tags', action='append', nargs='*', help="tags to add to the event", default=[])
    parser.add_option('-f', '--fields', dest='fields', nargs='*', metavar='field=value', action='append', help="fields to add to the event, FIELD=VALUE, separated by spaces", default=[])
    parser.add_option('-s', '--source-path', dest='source_path', help="specify the @source_path field, defaults to 'stdin'", default='stdin')
    parser.add_option('-S', '--source-host', dest='source_host', help="specify the @source_host field, defaults to the machine's FQDN", default=socket.getfqdn())
    parser.add_option('-O', '--stdout', dest='stdout', help="print read lines to stdout as well as to redis", action="store_true")
    parser.add_option('-v', '--verbose', dest='verbose', help="enable verbose mode", action="store_true")
    parser.add_option('-q', '--queue-size', dest='queue_size', help="set the maximum size for the internal queue in number of messages, defaults to 10000", default=10000, type="int")
    parser.add_option('-B', '--block', dest='block', help="block reads if the queue is full. defaults to False", default=False, action='store_true')
    options, _ = parser.parse_args()

    if not options.type:
        parser.error('-t|--type is a required argument')

    # set source
    options.source = "file:///{0}/{1}".format(options.source_host, options.source_path)

    # parse out fields
    fields = {}
    for fieldargs in options.fields:
        for fullfield in fieldargs:
            a,_,b = fullfield.partition("=")
            fields[a] = b
    options.fields = fields

    # flatten tags array
    tags = []
    for tagargs in options.tags:
        for tag in tagargs:
            tags.append(tag)
    options.tags = tags

    # verbose output
    if options.verbose:
        def verbose(s):
            print >> sys.stderr, s
    else:
        def verbose(s):
            pass

    return options
