from dataclasses import dataclass
import logging
from datetime import datetime
from pathlib import Path


@dataclass
class sjuLog():
    logtime: str
    logger: logging.Logger
    logformat: logging.Formatter 
    logfilepath: Path
    bufferlogs: bool 
    logbuffer: list 

    def __init__(self,  logname:str = 'sqljin', 
                        logfolderpath:Path = '../appcode/logs',
                        logfiletemplate:str = 'applog.{time}.txt',
                        bufferlogs: bool = False) -> None:
        if logfiletemplate.strip() == '': logfiletemplate = 'applog.{time}.log'
        self.logbuffer = []
        self.bufferlogs = bufferlogs
        self.setup(logname, logfolderpath, logfiletemplate)

    def setup(self, logname:str = 'sqljin', logfolderpath:Path = '../appcode/logs', logfile:str = '{logname}.applog.{time}.txt') -> logging.log:
        self.set_logtime()
        self.logformat = logging.Formatter('%(name)s %(asctime)s %(levelname)s:  %(message)s' , "%Y-%m-%d %H:%M:%S")
        self.logfilepath = Path(str(Path(logfolderpath) / logfile).replace('{time}', self.logtime).replace('{logname}', logname)).resolve()
    
        self.logfilepath.parents[0].mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(logging.DEBUG)

        self.info('sjuLog class instantiated and setup')
        return self.logger
        

    def debug(self, msg:str, *args) -> None:
        if self.bufferlogs: self.logbuffer.append([10, msg])
        else: self.logger.debug('  ' + msg, *args)

    def info(self, msg:str, *args) -> None:
        if self.bufferlogs: self.logbuffer.append([20, msg])
        else: self.logger.info('   ' + msg, *args)

    def warning(self, msg:str, *args) -> None:
        if self.bufferlogs: self.logbuffer.append([30, msg])
        else: self.logger.warning(msg, *args)

    def error(self, msg:str, *args) -> None:
        if self.bufferlogs: self.logbuffer.append([40, msg])
        else: self.logger.error('  ' + msg, *args)

    def header(self, msg:str, *args) -> None:
        msgs = ['', '-' * 90, ' ' * 10 + msg, '-' * 90, '']
        msg = '\n'.join(msgs)
        if self.bufferlogs: self.logbuffer.append([20, msg])
        else: self.logger.info('   ' + msg, *args)

    def dictlog(self, msg:dict, *args) -> None:
        pass

    def log(self, msg:str, msglevel:int=10) -> None:
        if msglevel==10:     self.debug(msg)
        elif msglevel==20:    self.info(msg)
        elif msglevel==30: self.warning(msg)
        elif msglevel==40:   self.error(msg)
        else: 
            self.logger.error('logger registered a malformed entry: level=%i, msg=%s' %(msglevel, msg))
        return None 

    def unbuffer(self) -> None:
        self.bufferlogs = False
        for lg in self.logbuffer:
            self.log(msg=lg[1], msglevel=lg[0])
        self.logbuffer = list()

    def set_logtime(self, strtimeFormat:str = '') -> str: 
        if strtimeFormat is None or strtimeFormat=='':
            self.logtime = str(datetime.now().strftime("%Y%m%d-%H%M%S")) 
        else:
            self.logtime = str(datetime.now().strftime(strtimeFormat))
        return self.logtime

    def clear_handlers(self) -> None:
        self.logger.handlers.clear

    def create_stream_handler(self) -> None:
        shandler = logging.StreamHandler()
        shandler.setFormatter(self.logformat)
        shandler.setLevel(logging.DEBUG)
        self.logger.addHandler(shandler)
        self.info('logging handler added for streaming')

    def create_file_handlers(self, logfilepath:Path='') -> None:
        lfpath = self.logfilepath if logfilepath=='' else logfilepath
        fhandler = logging.FileHandler(lfpath)
        fhandler.setFormatter(self.logformat)
        fhandler.setLevel(logging.DEBUG)
        self.logger.addHandler(fhandler)
        self.info('logging handler added for file: %s' %lfpath)

    def create_default_handlers(self) -> None:
        self.create_stream_handler()
        self.create_file_handlers()




# tests
if __name__ == '__main__':
    log = sjuLog('COA-AppLog','../appcode/logs', bufferlogs=True)
    log.create_default_handlers()
    # log.create_stream_handler()  # stream to console, not file

    # buffering logs allows logging before logging is configured
    for x in range(1,10):
        log.info('this is a pre-log setup message # %i' %x)
    x+=1
    log.unbuffer()
    
    log.info('First RealTime Log')
    log.debug('logging test has commenced!')
    log.error('Doh!  Error, out of donuts!')
    log.log('generic log for wierd assignements - valid level', 20)
    log.log('generic log for wierd assignements - invalid level', 23)
    log.warning('Final Log')
