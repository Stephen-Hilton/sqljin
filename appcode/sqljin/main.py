print(f'loaded {__name__}')

import sys, os
from pathlib import Path 
import util

# setup logging and path class
paths = util.sj_paths.sj_Paths()
log = util.sj_logger.sj_Logger(paths)
log.header(f'WELCOME TO {paths.appname.upper()}!')
log.info('application environment paths:\n\t' + '\n\t'.join( [str(x) for x in sys.path]))


# setup event framework:
event = util.sj_event.sj_Event(log)
log.info('event framework starting...')
event.setup_logging_events()
broadcast = event.broadcast
add_handler = event.add_handler
log.debug('testing event framework...')
broadcast('test', 'event framework working')


if Path(paths.localPath / 'config.db').exists(): 
    os.remove( Path(paths.localPath / 'config.db') )  # just for testing...


# load local config.db from sqlite
config_local = util.sj_configdb.sj_Config(event, 'Local', 1)



# choose which UI to start based on commandline arg:
sys.argv.append('updater')
uistart = 'updater' if 'updater' in sys.argv else 'main'


log.header('Application Complete, Closing')