print(f'loaded {__name__}')

import sys, os
from pathlib import Path

import dbConn.dbconn_sqlite as dbConnSQLite

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject  
import objects.sj_orgs     as sjorg  


## --------------------------------
## Initial Utility Setup:
## --------------------------------
# setup logging and path class
paths = sjpaths.sj_Paths()
log = sjlog.sj_Logger(paths)
log.header(f'WELCOME TO {paths.appname.upper()}!')
log.info('application environment paths:\n\t' + '\n\t'.join( [str(x) for x in sys.path]))

# setup event framework:
event = sjevent.sj_Event(log)
event.setup_logging_events()
broadcast = event.broadcast
add_handler = event.add_handler
log.debug('testing event framework...')
broadcast('test', 'event framework working')

# bundle utilities for easier passing around
utils = {'log':log, 'event':event, 'paths':paths}


## --------------------------------
## Initialize all Factories (and event handlers)
## --------------------------------
orgfactory = sjorg.sj_OrgFactory(utils)


event.broadcast('app.started')



## --------------------------------
## Demonstrate basic functionality needed for UI:
## --------------------------------

# create new org:
event.broadcast('user.request.new.org', 'Alpha')
event.broadcast('user.request.new.org', 'Bravo')
event.broadcast('org.new', 'Charlie')
event.broadcast('org.new', 'Local')
event.broadcast('org.new', 'Global')

event.broadcast('user.request.new.Alpha.system', 'Transcend_Alpha')

# event.print_handlers_to_log()

log.header('Application Complete, Closing')