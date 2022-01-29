print(f'loaded {__name__}')

import logging
from pathlib import Path

class sj_Logger(logging.Logger):
    paths: Path 

    def __init__(self, paths:object, *args, **kwargs) -> None:
        self.paths = paths
        self.name = self.paths.appname
        super().__init__(self.name, *args, **kwargs)

        self.logformatter = logging.Formatter("%(name)s %(asctime)s %(levelname)8s -- %(message)s", "%Y-%m-%d %H:%M:%S")

        shandler = logging.StreamHandler()
        shandler.setFormatter(self.logformatter)
        shandler.setLevel(logging.DEBUG)
        self.addHandler(shandler)

        fhandler = logging.FileHandler(self.paths.applogfilePath)
        fhandler.setFormatter(self.logformatter)
        fhandler.setLevel(logging.DEBUG)
        self.addHandler(fhandler)

    def header(self, msg):
        self.info('='*60)
        self.info(str(msg).upper())
        self.info('='*60)

    def line(self):
        self.info('-'*60)

    def ui(self, msg):
        self.info('(ui-log) %s' %msg)

    def tbd(self, msg):
        self.warning('(TBD) %s' %msg)

    def sql(self, msg:str):
        msglist = msg.strip().split('\n')
        if msglist[0].strip()  != '': 
            msglist.insert(0,'')
            msglist.insert(0,'')
        if msglist[-1].strip() != '': msglist.append('')
        msg = 'generated sql:' + '\n'.join(['    ' + str(m).strip() for m in msglist])
        self.debug(msg)




