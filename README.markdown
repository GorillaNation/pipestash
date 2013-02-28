# pipestash

Pipestash is a tool which will read lines from stdin, format them as logstash `json_event` events, and throw them into a redis list for consumption by a logstash agent.

The design philosophy is to try *really* hard not to lose any messages, and also to try not to block the process being piped into pipestash. And also be able to handle transient failures of the upstream redis server, and also to notify the end user should we end up actually having to drop messages.

# other backends
Support for other backends is not planned, but if you would like to submit a pull request, I'm willing to take a look, however this should be simple enough for you to just write your own :)

Additionally, support for other redis types is not currently planned, but I'll entertain pull requests

# command line arguments

	-t | --type TYPE

the type to add to the json\_event. has no default and is a required argument.

	-r | --redis-url REDIS_URL

the URL of the redis server/database to write events to. Defaults to `redis://localhost:6379/0`

	-R | --redis-key REDIS_KEY

the redis key to append log events to. Defaults to 'logstash'

	-T | --tags tag1 [tag2] [...]

tags to add to the json\_event object

	-f | --fields field1=value1 [field2=value2] [...]

fields and values to add to the json\_event object

	-s | --source-path

the `@source_path` to place in the json\_event object. defaults to stdin

	-S | --source-host

the `@source_host` to place in the json\_event object. defaults to the machine's FQDN

	-O | --stdout

print incoming lines to stdout as well. This is useful if you would also like to log lines with something like [multilog](http://cr.yp.to/daemontools/multilog.html "djb's multilog")

	-v | --verbose

enable verbose output

	-q | --queue-size

maximum size of internal queue before pipestash starts dropping messages

# internal queueing mechanism

In order to try to prevent the process writing into pipestash from blocking during intermittent redis issues or spikes of incoming messages, pipestash employs an internal queueing mechanism.

To prevent blocking in the case of queue overflow, pipestash simply start dropping messages on the floor. However, it will keep track of the number of dropped messages and the first time it dropped one and keep trying to queue a message about that until things recover, when it then resets.

I thought quite a bit about this issue, and I realized that a line was going to have to be drawn where we were either going to start blocking the upstream

Upon some simple testing (the SleepyOutput plugin was written specifically for this) with about 100k apache log messages in the queue, memory usage of pipestash was about 96. I'm *very* interested in lowering the memory usage here, as 100k messages is only about 25 minutes of logs on one of our busiest sites, so I'd like to be able to handle longer redis outages / issues without being forced to drop messages or have unreasonable memory usage from pipestash. I started by having pipestash build the json\_event prior to placing the message into the queue, which took about 104MB for 100k messages, so instead I was letting the consumer build the event and the producer just put a timestamp and the raw message into the queue. Clearly, it didn't seem to change the memory usage very much, so I'm not entirely sure what to do about that! I could have sworn I had a test once that had 1 million messages in the queue and was only taking ~35MB of memory, so I need to figure out what I was doing there or if maybe I was just incorrect in my testing.

