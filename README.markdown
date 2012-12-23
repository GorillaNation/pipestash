# pipestash

Pipestash is a tool which will read lines from stdin, format them as logstash `json\_event` events, and throw them into a redis list for consumption by a logstash agent.

Support for other backends is not planned, but if you would like to submit patches, I'm willing to take a look, however this should be simple enough for you to just write your own :)

Additionally, support for other redis types is not currently planned, but I'll accept patches.

# command line arguments

	-o | --output TYPE

the output type. defaults to redis, which is also the only type :)

	-u | --url REDIS_URL

the URL of the redis server/database to write events to. Defaults to `redis://localhost:6379/0`

	-k | --key KEY

the redis key to write events to. defaults to `logstash`

	-K | --key-type KEYTPE

the redis key type. Defaults to list, which is also the only currently supported key type.

	-T | --tags tag1 [tag2] [...]

tags to add to the json\_event object

	-f | --fields field1=value1 [field2=value2] [...]

fields and values to add to the json\_event object

	-t | --type TYPE

the type to add to the json\_event. has no default and is a required argument.
