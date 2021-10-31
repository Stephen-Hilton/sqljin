from pathlib import Path
from dataclasses import dataclass

try:
    from sqljin.sjuLog import sjuLog
except:
    from sjuLog import sjuLog


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
        
        objname, obj, kwargs, data = self.unpack_data(data)
        
        # confirm the event exists as a registered handler:
        if not eventname in self.handlers:
            self.log.warning(f'EVENT "{eventname}" was broadcast by "{objname}", but has no handlers / listeners')
            return None

        # has a handler, so log and send the data off to the correct function(s) for execution   
        self.log.debug(f'EVENT "{eventname}" was broadcast by "{objname}", picked up by {len(self.handlers[eventname])} handlers')
        rtn = []
        for fn in self.handlers[eventname]:
            rtn.append( fn(data) )
        return rtn
        

    def pack_data(self, sjoObject:object, **kwargs) -> dict:
        return {'object':sjoObject, 'kwargs':kwargs }

    def unpack_data(self, data=None):
        obj = None
        kwargs = {} 
        objname = Path(__file__).stem
        if type(data) is dict:
            if 'kwargs' in data: kwargs = data['kwargs']
            if 'object' in data:
                obj = data['object']
                if 'name' in kwargs:  objname = kwargs['name']
                elif 'name' in obj.__dict__: objname = obj.name 
                elif 'parent' in obj.__dict__ and 'name' in obj.parent.__dict__:  objname = obj.parent.name
            data['kwargs'] = kwargs
            data['object'] = obj 
        kwargs['name'] = objname
        return objname, obj, kwargs, data 
        



# testing:
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