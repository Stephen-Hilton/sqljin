import logging
from datetime import datetime
from pathlib import Path


def logging_start(logname:str = 'sqljin', logfilepath:Path = '../appcode/logs/sqljin.{time}.txt'):
    logts = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
    logpath = Path(str(logfilepath.resolve()).replace('{time}', logts))    
    logpath.parents[0].mkdir(parents=True, exist_ok=True)
    
    log = logging.getLogger(logname)
    logformat: logging.Formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:  %(message)s')
    log.setLevel(logging.DEBUG)
    
    log.handlers.clear

    shandler = logging.StreamHandler()
    shandler.setFormatter(logformat)
    shandler.setLevel(logging.DEBUG)
    log.addHandler(shandler)

    fhandler = logging.FileHandler(logpath)
    fhandler.setFormatter(logformat)
    fhandler.setLevel(logging.DEBUG)
    log.addHandler(fhandler)

    return log


if __name__ == '__main__':
    filepath = Path('../appcode/logs/applog.{time}.txt')
    log = logging_start('sqljin', filepath)
    log.info('First Log')
    log.debug('logging test has commenced!')
    log.warning('Final Log')
