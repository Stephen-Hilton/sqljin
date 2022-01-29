print(f'loaded {__name__}')

# BUILD EVENT FRAMEWORK
# event convension:  action.type.name  or  action.type.parent.name
# request is current tense, notifications are past tense
#    some examples:
#           update.system.teradata
#           updated.system.teradata
#           load.collection.teradata.metrics
#           loaded.collection.teradata.solutions
#           get.db.global.variables
#           got.db.global.variables
#           updated.system.teradata.variables

from .sj_logger import sj_Logger

class sj_Event():
    handlers = {}
    log: sj_Logger
    debug_events:bool = False

    def __init__(self, log:sj_Logger) -> None:
        self.log = log

    def add_handler(self, eventname:str, fn):
        if not eventname in self.handlers:
            self.handlers[eventname] = []
        if fn not in self.handlers[eventname]:
            self.handlers[eventname].append(fn)
            self.log.debug('new event handler "%s" registered to listen for event "%s"' %(str(fn.__name__), eventname))
        else:
            self.log.warning('event handler found duplicate function per event, ignoring to prevent duplication')

    def broadcast(self, eventname:str, *args, **kwargs) -> list:            
        # confirm the event exists as a registered handler:
        if not eventname in self.handlers:
            self.log.warning(f'EVENT "{eventname}" was broadcast, but has no handlers / listeners')
            return None

        # if has a handler, log and send the data off to the correct function(s) for execution   
        if eventname[:3] != 'log':
            handlerstring =  "(%s)" %str(', '.join([f.__name__ for f in self.handlers[eventname] ]))
            self.log.debug(f'EVENT "{eventname}" was broadcast and picked up by functions: {handlerstring}')
        rtn = []
        for fn in self.handlers[eventname]:
            rtn.append( fn(*args, **kwargs) )
        return rtn
        
    def setup_logging_events(self):
        self.log.debug('doing initial event handler population')
        # add logging events
        self.add_handler('print', print )
        self.add_handler('test', self.log.debug )
        self.add_handler('log', self.log.debug )
        self.add_handler('log.debug', self.log.debug )
        self.add_handler('log.info', self.log.info )
        self.add_handler('log.warning', self.log.warning )
        self.add_handler('log.error', self.log.error )
        self.add_handler('log.critical', self.log.critical )
        self.add_handler('log.header', self.log.header)
        self.add_handler('log.ui', self.log.ui)
        self.add_handler('log.ui.updater', self.log.ui)
        self.add_handler('log.ui.main', self.log.ui)
        self.add_handler('log.tbd', self.log.tbd)

    def print_handlers_to_log(self):
        self.log.debug('print out of all event handlers:')
        for e, fn in self.handlers.items():  
            fns = ', '.join( [f.__name__ for f in fn] ) 
            print('    ', e, '=', f"({fns})")

