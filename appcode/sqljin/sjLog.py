import logging
from datetime import datetime

logts = str(datetime.now().strftime("%Y%m%d-%H%M%S"))


def logging_start(logname:str = 'sqljin'):
    log = logging.getLogger(logname)
    logformat: logging.Formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:  %(message)s')
    log.setLevel(logging.DEBUG)

    return log


def addhandler(logname:str, handlename:str = '', loglevel:int = logging.INFO, logfilepath:str='' ) -> logging.FileHandler:
    hname = logfilepath if name == '' else name
    ts = timestamp
    hlogfilepath = str(logfilepath).replace(r'{time}', ts).replace(r'{ts}', ts).replace(r'{timestamp}', ts)

    if hlogfilepath == '':
        handler = logging.StreamHandler()
        htype = 'streaming'
    else:
        handler = logging.FileHandler(hlogfilepath, 'w+')
        htype = 'file'

    handler.setFormatter(self.logformat)
    handler.setLevel(hlvl)
    self.log.addHandler(handler)
    self.logHandlers[hname] = handler
    return handler

log = start_logging()

if __name__ == '__main__':
    pass

