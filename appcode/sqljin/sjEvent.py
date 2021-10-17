
handlers = dict()

def add_handler(eventname:str, fn):
    if not eventname in handlers:
        handlers[eventname] = []
    handlers[eventname].append(fn)

def broadcast(eventname:str, data):
    if not eventname in handlers:
        # log.WARNING('No Handler for event: %s' %eventname)
        return None
    for fn in handlers[eventname]:
        fn(data)

def handles(eventname:str, fn):
    def wrapper(*args, **kwargs):
        print('start')
        print(eventname)
        fn(*args, **kwargs)
        print('end')
    return wrapper



if __name__ == '__main__':
    add_handler('print', print )
    broadcast('print', 'this is a test of event based print')
    broadcast('print', 'whoo hoo!')
    
    @handles('print')
    def dostuff(msg):
        print(msg)

    dostuff('doing stuff')

    