from pathlib import Path 
from sqljin.sjLog import logging_start
import sqljin.sjEvent as event

log = logging_start('sqljin', Path('./logs/applog.{time}.txt'))
log.info('Application Started')

event.add_handler('print', print)
event.broadcast('print', 'the App has started')
event.broadcast('non-event')

log.info('Application Finished')