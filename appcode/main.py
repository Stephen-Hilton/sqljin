from sqljin.sjLog import logging_start
import sqljin.sjEvent as event
import sqljin.sjConfig as config
from sqljin.sjPath import sjPath


# load paths 
paths = sjPath(__file__)
print(paths.appname)



# load config files
config.configs_load()



# setup logging:
log = logging_start('sqljin', paths.appcode.path('logs'), 'applog.{time}.txt')
log.info('Application Started')

# setup event framework:
event.add_handler('print', print)
event.broadcast('print', 'the App has started')
event.broadcast('non-event')

log.info('Application Finished')