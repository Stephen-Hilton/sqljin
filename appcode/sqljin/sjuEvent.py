from pathlib import Path
from dataclasses import dataclass

@dataclass
class sjuEvent():
    handlers: dict()
    log: object 

    def __init__(self, logger:object):
        self.log = logger
        self.handlers = {}
        self.log.info('sjevent class instantiated')

    def add_handler(self, eventname:str, fn):
        if not eventname in self.handlers:
            self.handlers[eventname] = []
        self.handlers[eventname].append(fn)
        self.log.info(f'new event handler "%s" registered to listen for event "%s"' %(str(fn.__name__), eventname))

    def broadcast(self, eventname:str, data=None) -> list:
        if not eventname in self.handlers:
            self.log.warning(f'event "{eventname}" was broadcast, but has no handlers / listeners')
            return None
        self.log.debug('event "%s" was broadcast, picked up by %i handlers' %(eventname, len(self.handlers[eventname])))
        rtn = []
        for fn in self.handlers[eventname]:
            rtn.append( fn(data) )
        return rtn



if __name__ == '__main__':
    from sjuLog import sjuLog
    log = sjuLog('test')
    log.create_stream_handler()
    log.debug('Logging started')
    log.info('Setting Up Event Framework')

    event = sjuEvent(log)  # requires logging
    event.add_handler('print', print )
    event.add_handler('log.warn', log.warning )
    event.add_handler('log.warn', log.error )
    event.add_handler('log', log.debug )
    event.broadcast('print', 'this is a test of event based print')
    event.broadcast('log.warn', 'This event has two handlers, you should see this message twice.')
    event.broadcast('log', 'Super Test')
    event.broadcast('poopypants')

    event.add_handler('logtime', log.set_logtime)
    print(event.broadcast('logtime'))