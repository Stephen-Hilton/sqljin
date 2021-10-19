from pathlib import Path

handlers = dict()


def add_handler(eventname:str, fn):
    if not eventname in handlers:
        handlers[eventname] = []
    handlers[eventname].append(fn)

def broadcast(eventname:str, data=None):
    if not eventname in handlers:
        # TODO: add goddamn logging
        # log.warning('No Handler for event: %s' %eventname)
        return None
    for fn in handlers[eventname]:
        fn(data)

def handles(eventname:str, fn):  # this is not working currently
    def wrapper(*args, **kwargs):
        print('start')
        print(eventname)
        fn(*args, **kwargs)
        print('end')
    return wrapper



if __name__ == '__main__':
    from sjLog import logging_start
    log = logging_start('sqljin', Path('./logs/applog.{time}.txt'))
    log.info('Setting Up Event Framework')
    add_handler('print', print )
    add_handler('log.warn', log.warn )
    add_handler('log.warn', log.error )
    add_handler('log', log.debug )
    broadcast('print', 'this is a test of event based print')
    broadcast('log.warn', 'whoo hoo!')
    broadcast('log', 'Super Test')
    broadcast('poopypants')

    