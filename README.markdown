# pipestash

Pipestash is a tool which will read lines from stdin, format them as logstash `json\_event` events, and throw them into a redis list for consumption by a logstash agent.

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

the `@source\_path` to place in the json\_event object. defaults to stdin

	-S | --source-host

the `@source\_host` to place in the json\_event object. defaults to the machine's FQDN

	-O | --stdout

print incoming lines to stdout as well. This is useful if you would also like to log lines with something like [multilog](http://cr.yp.to/daemontools/multilog.html "djb's multilog)

	-v | --verbose

enable verbose output
