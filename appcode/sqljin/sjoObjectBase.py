from pathlib import Path
from dataclasses import dataclass
import json

try:
    from sqljin.sjuLog import sjuLog
    from sqljin.sjuEvent import sjuEvent
    from sqljin.sjuPath import sjuPath
    from sqljin.sjuUtil import sjuUtil
except:
    from sjuLog import sjuLog
    from sjuEvent import sjuEvent
    from sjuPath import sjuPath
    from sjuUtil import sjuUtil


@dataclass
class sjoObjectBase():
    util: sjuUtil
    log: sjuLog
    name: str 
    type: str
    version: str
    prefix: str
    filepath: Path
    parent: object
    variables: object

    def __init__(self, util: sjuUtil, filepath: Path, parent: object = None):
        self.util = util
        self.filepath = filepath
        self.name = Path(filepath).stem
        self.type = type(self).__name__
        self.parent = parent 
        self.prefix = '%s.%s: ' %(self.type, self.name)
        self.log = self.objlogger(util.log, self.prefix)
        self.variables = self.objvariables(self, self.filepath / 'variables.json')
        self.log.debug('class intantiated from filepath %s' %self.filepath)

    def register_handlers(self) -> None:
        event = self.util.event
        prefix = self.prefix.strip()[:-1]
        event.add_handler(prefix + '.load', self.load)
        event.add_handler(prefix + '.execute', self.execute)

    def load(self) -> None:
        self.log.debug('loading / reloading object')
        self.register_handlers()
        self.variables.load()

    def new(self) -> None:
        self.log.debug(f'creation of new {self.type} started for {self.name}')
        if self.filepath.exists():
            self.log.error(f'{self.type} {self.name} already exists, aborting creation of new (like a highlander, there can be only one)')
            return None
        else:
            self.filepath = self._new()
            self.log.info(f'new {self.type} called {self.name} created')
            return None


    def _new(self) -> Path:
        return self.filepath.mkdir(parents=True, exist_ok=True)

    def execute(self) -> dict:
        self.log.info('Execution Started')
        rtn = self._execute()
        self.log.info(f'Execution Complete: {str(rtn)}')

    def _execute(self) -> dict:
        return {'status':'success!'}

    class objlogger():
        log: sjuLog
        logprefix: str ='' 
        def __init__(self, logger: sjuLog, logprefix:str) -> None:
            self.log = logger
            self.logprefix = logprefix 
        def debug(self, msg:str, *args) -> None:
            self.log.debug(self.logprefix + str(msg), *args)
        def info(self, msg:str, *args) -> None:
            self.log.info(self.logprefix + str(msg), *args)
        def warning(self, msg:str, *args) -> None:
            self.log.warning(self.logprefix + str(msg), *args)
        def error(self, msg:str, *args) -> None:
            self.log.error(self.logprefix + str(msg), *args)
        def header(self, msg:str, *args) -> None:
            self.log.header(self.logprefix + str(msg), *args) 
        def dictlog(self, msgdict:dict, *args) -> None:
            self.log.dictlog(msgdict, *args) 
    
    class objvariables():
        fulldict: dict
        variables: dict
        version: str
        filepath: Path 
        default: dict 
        downloadable: bool = False
        disabled: bool = False

        def __init__(self, parent:object, filepath:Path, default:dict = {} ):
            self.parent = parent 
            self.log = parent.log
            self.filepath = filepath
            self.default = default
            self.fulldict = {}
            self.variables = {}
            self.version = 0
            if self.default == {}: self.default = {"version":0, "variables":{}}
                
        def load(self) -> dict:
            if self.disabled: return None
            self.log.debug(f'loading variables')
            self.fulldict = self.parent.util.paths.getYaml(self.filepath, defaults=self.default)
            if len(self.fulldict) == 0: 
                self.log.error('variable file failed to load, try running the updater.')
            if 'version' in self.fulldict: self.version = str(self.fulldict['version'])
            if 'variables' in self.fulldict: self.variables = self.fulldict['variables']
            self.log.debug(f'variables set, version: {self.version} and variable dictionary:')
            self.log.dictlog(self.variables)
            return self.variables


        def clear(self) -> dict:
            if self.disabled: return None
            self.log.warning('resetting variables.json to default')
            self.fulldict = self.default
            return self.fulldict

        def save(self) -> None:
            if self.disabled: return None
            with open(self.filepath, 'w') as fh:
                json.dump(self.fulldict, fh, indent=4)
            self.log.warning('saved variables to variables.json')

        def add_item(self, key:str, value):
            if self.disabled: return None
            self.variables[key] = value

        def remove_item(self, key:str):
            if self.disabled: return None
            if key in self.variables: del self.variables[key]

        def get_item(self, key:str, default:str = "missing"):
            if self.disabled: return None
            return self.variables[key] if key in self.variables else default


            
        



if __name__=='__main__':
    util = sjuUtil()
    obj = sjoObjectBase(util, Path(r"C:\git\sqljin\configs\organizations\Teradata\Collections\Metrics"))
    obj.load()
    obj.variables.default = {"version":0, "variables":{"something":"Awesome!!!"}}
    # obj.variables.add()