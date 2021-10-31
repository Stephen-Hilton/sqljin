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
    event: sjuEvent
    paths: sjuPath
    name: str 
    type: str
    eventprefix: str
    version: str
    filepath: Path
    parent: object
    variables: object 

    def __init__(self, util: sjuUtil, filepath: Path, parent: object = None):
        self.util = util
        self.event = util.event
        self.paths = util.paths
        self.type = type(self).__name__
        self.parent = parent 
        self.eventprefix = self.type
        self.yamldefault = {"version":0, "variables":{}}
        
        self.name = Path(filepath).stem         
        self.filepath = Path(filepath / 'sjoDefinition.yaml') if filepath.is_dir() else Path(filepath)
        self.log = self.objlogger(util.log, '%s.%s: ' %(self.type, self.name))
        
        self.log.debug(f'{self.type}.{self.name} intantiated from filepath %s' %self.filepath)
        self.register_handlers()
        self.event.broadcast(f'{self.eventprefix}.created', self.event.pack_data(self) )
        

    def register_handlers(self) -> None:
        self.event.add_handler(self.eventprefix + '.load', self.load)
        self.event.add_handler(self.eventprefix + '.execute', self.execute)

    def load(self) -> None:
        self.log.debug('loading / reloading object')
        yamldict = self.paths.loadYaml(self.filepath, self.yamldefault)
        self._load()
        self.variables = self.objvariables(self, yamldict['variables']) 
        self.event.broadcast(f'{self.eventprefix}.loaded', self.event.pack_data(self) )

    def _load(self) -> None:
        pass


    def updatecheck(self):
        self.event.broadcast(self.eventprefix + '.updatecheck', self.event.pack_data(self) )


    def execute(self) -> dict:
        self.log.info('Execution Started')
        rtn = self._execute()
        self.log.info(f'Execution Complete: {str(rtn)}')

    def _execute(self) -> dict:
        return {'status':'success!'}

    class objlogger():
        log: sjuLog
        prefix: str ='' 
        def __init__(self, logger: sjuLog, logprefix:str) -> None:
            self.log = logger
            self.prefix = logprefix 
        def debug(self, msg:str, *args) -> None:
            self.log.debug(self.prefix + str(msg), *args)
        def info(self, msg:str, *args) -> None:
            self.log.info(self.prefix + str(msg), *args)
        def warning(self, msg:str, *args) -> None:
            self.log.warning(self.prefix + str(msg), *args)
        def error(self, msg:str, *args) -> None:
            self.log.error(self.prefix + str(msg), *args)
        def header(self, msg:str, *args) -> None:
            self.log.header(self.prefix + str(msg), *args) 
        def dictlog(self, msgdict:dict, *args) -> None:
            self.log.dictlog(msgdict, *args) 
    
    class objvariables():
        variables: dict = {}

        def __init__(self, parent:object, variabledict:dict ):
            self.parent = parent 
            self.log = parent.log
            self.event = parent.event
            self.paths = parent.paths
            self.load(variabledict)
                
        def load(self, variabledict:list) -> dict:
            self.log.debug(f'loading variables')
            for n,v in variabledict.items():
                self.set_item(n,v)
            self.log.debug(f'variables set with {len(self.variables)} items found:')
            self.log.dictlog(self.variables)
            self.event.broadcast('%s.variables.changed' %self.parent.eventprefix, self.event.pack_data(self.parent, change='loaded') )
            return self.variables

        def clear(self) -> dict:
            self.log.warning('clearing all variables')
            self.variables = {}
            self.event.broadcast('%s.variables.changed' %self.parent.eventprefix, self.event.pack_data(self.parent, change='cleared') )
            return self.fulldict

        def set_item(self, key:str, value):
            self.variables[key] = value
            self.log.debug(f'variable {key} set to {value}')
            self.event.broadcast('%s.variables.changed' %self.parent.eventprefix, self.event.pack_data(self.parent, change='set_item') )
            return value 

        def get_item(self, key:str, default:str = "missing"):
            if key in self.variables:
                rtn = self.variables[key]
            else:
                rtn = default
                self.parent.event.broadcast('%s.variable.sentdefault' %self.parent.type, self.parent.event.pack_data(self, str(tuple(key,rtn)), key=key, default=rtn)) 
            return rtn

        def getset_item(self, key:str, default:str):
            return self.set_item(key, self.get_item(key, default))

        def remove_item(self, key:str) -> bool:
            saygoodbyeto = ''
            if key in self.variables: 
                saygoodbyeto = str(self.variables[key])
                del self.variables[key]
            if key in self.__dict__:
                saygoodbyeto = str(self.variables[key])
                del self.variables[key]
            if len(saygoodbyeto)>0:
                self.event.broadcast('%s.variables.changed' %self.parent.eventprefix, self.event.pack_data(self.parent, change='remove_item', key=key, value_removed=saygoodbyeto) )
                return True
            return False




if __name__=='__main__':
    util = sjuUtil()
    obj = sjoObjectBase(util, Path(r"C:\git\sqljin\configs\Global\systems\Transcend.yaml"))
    obj.load()
    # obj.variables.add()