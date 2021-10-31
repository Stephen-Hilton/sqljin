from dataclasses import dataclass
from logging import exception
# local testing vs remote calls

try:
    from sqljin.sjuLog import sjuLog
    from sqljin.sjuEvent import sjuEvent
    from sqljin.sjuPath import sjuPath
except:
    from sjuEvent import sjuEvent
    from sjuPath import sjuPath
    from sjuLog import sjuLog


## Wrapper class to ease passing around log, paths, events
@dataclass
class sjuUtil():
    log: sjuLog
    event: sjuEvent
    paths: sjuPath
    _appname: str
    
    def __init__(self) -> None:
        self.load()

    def load(self):

        # start pre-logging before logging is fully setup:
        self.log = sjuLog(bufferlogs=True)
        self.log.header('Utility Classes Loading')
        self.log.warning('logging started (obviously)')

        # setup event framework:
        self.event = sjuEvent(self.log)  # requires logging
        self.event.add_handler('log', self.log.info)
        self.event.broadcast('log', 'Event framework started and active')

        # load paths 
        self.paths = sjuPath(__file__, self.log, self.event)
        str(self.paths) # this triggers the built-in logging
        self.appname = self.paths.appname
    
        # finish setting up logging now that we now where we are:
        self.log.setup( self.paths.appname, self.paths.appcode.path('logs'))
        self.log.create_default_handlers()
        self.log.unbuffer()




    @property
    def appname(self) -> str:
        return self._appname

    @appname.setter
    def appname(self, v: str) -> None:
        self._appname = v
        self.paths.appname = v



if __name__=='__main__':
    # all it takes to start the app:    
    util = sjuUtil()
