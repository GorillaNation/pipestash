import socket
import optparse

def parseargs():
    def parse_field_args(option, opt_str, value, parser):
        args=[]
        for arg in parser.rargs:
            if arg[0] != "-":
                args.append(arg)
            else:
                del parser.rargs[:len(args)]
                break
        if getattr(parser.values, option.dest):
            args.extend(getattr(parser.values, option.dest))
        setattr(parser.values, option.dest, args)

    # parse command line
    parser = optparse.OptionParser()
    parser.add_option('-t', '--type', dest='type', help='the event type (required)')
    parser.add_option('-r','--redis-url', dest='redis_url', help="specify the URL of the redis database to use, defaults to redis://localhost:6379/0", default='redis://localhost:6379/0')
    parser.add_option('-R', '--redis-key', dest='redis_key', help="redis key to add events to, defaults to logstash", default='logstash')
    parser.add_option('-T','--tags', dest='tags', action='callback', callback=parse_field_args, help="tags to add to the event", default=[])
    parser.add_option('-f', '--fields', dest='fields', action='callback', callback=parse_field_args, metavar='field=value', help="fields to add to the event, FIELD=VALUE, separated by spaces", default=[])
    parser.add_option('-s', '--source-path', dest='source_path', help="specify the @source_path field, defaults to 'stdin'", default='stdin')
    parser.add_option('-S', '--source-host', dest='source_host', help="specify the @source_host field, defaults to the machine's FQDN", default=socket.getfqdn())
    parser.add_option('-O', '--stdout', dest='stdout', help="print read lines to stdout as well as to redis", action="store_true")
    parser.add_option('-v', '--verbose', dest='verbose', help="enable verbose mode", action="store_true")
    parser.add_option('-q', '--queue-size', dest='queue_size', help="set the maximum size for the internal queue in number of messages, defaults to 10000", default=10000, type="int")
    parser.add_option('-B', '--block', dest='block', help="block reads if the queue is full. defaults to False", default=False, action='store_true')
    parser.add_option('-w', '--timeout', dest='timeout', help="if pipestash is unable to connect to redis or redis runs OOM, put the consumer thread to sleep a random amount of time between `-w seconds` and +0 seconds. defaults to 20 seconds", default=20, type="float")
    parser.add_option('-n', '--nice', dest='nice', help="sets the niceness value of the process", default=5, type="int")
    options, _ = parser.parse_args()

    # required fields validation
    if not options.type:
        parser.error('-t|--type is a required argument')

    # set source
    options.source = "file:///{0}/{1}".format(options.source_host, options.source_path)

    # parse out fields
    fields = {}
    for fieldargs in options.fields:
        a,_,b = fieldargs.partition("=")
        fields[a] = b
    options.fields = fields

    # verbose output
    if options.verbose:
        def verbose(s):
            print >> sys.stderr, s
    else:
        def verbose(s):
            pass

    return options
