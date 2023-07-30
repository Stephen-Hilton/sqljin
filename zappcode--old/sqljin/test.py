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

# bundle utilities for easier passing around
utils = {'log':log, 'event':event, 'paths':paths}
event.add_handler('utils.GET', lambda:utils)




for fmt in ['m/d/yy h:m:s', 'yyyy-mm-dd hh:mm:ss', 'mm/dd/yyyy', 'hh:mm:ss', 'yyyymmdd_hhmmss', 'Excel', '24hh == 12hhp']:
    oldfmt = fmt.rjust(20,' ')
    newfmt = misc.translate_simple_dateformat(fmt)
    nowish = datetime.now()
    print(f'from {oldfmt}   to   {newfmt.ljust(25," ")}  looks like { nowish.strftime(newfmt)}')


log.header('Application Complete, Closing')