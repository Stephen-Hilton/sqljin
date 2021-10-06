from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import logging

from .event import subscribe, trigger
from .util import *

# logging options
initiator = 'system'
appname = 'sqljin'
log_detail_format = '%(asctime)s:%(levelname)s:%(appname)s:%(initiator)s:  %(message)s'
log_summary_format = '%(asctime)s:%(levelname)s:  %(message)s'

# create logging object
log = logging.LoggerAdapter(logging.getLogger(__name__), {'initiator':initiator, 'appname':appname})
log.setLevel(logging.DEBUG)
log.handlers.clear()
log.logger.handlers.clear()

# create logging event handlers
def log_add_handler(**kwargs):
    newhandler = find_first(['handler_object','handler'], kwargs, logging.StreamHandler)
    logformat = find_first(['log_format','format'], kwargs, log_detail_format, str)

    if newhandler: 
        newhandler.setFormatter(logformat)
        log.addHandler(newhandler)
        return newhandler
    else:
        return None

def log_clear_handlers(**kwargs) -> None:
    log.logger.handlers.clear()
    return None


# register handlers with event framework:
subscribe('log_add_handler', log_add_handler)
subscribe('log_clear_handlers', log_add_handler)


