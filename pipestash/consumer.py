# this function is the top level of the execution of the
# child process. I think that's how I'm gonna do it at least.

def consume(queue, output):
    for item in iter(queue.get, None):
        try:
            output.do(item)
        except:
            # FIXME: do something about exceptions
            pass
