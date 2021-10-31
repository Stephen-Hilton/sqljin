from pathlib import Path
from dataclasses import dataclass
import yaml

# setup logging back to same object

@dataclass
class sjuPath():
    appcode: object
    approot: object
    configs: object
    history: object
    orgs: object
    appname: str
    log: object 

    # subclass:
    class sjpathroot():
        _path:Path 
        def __init__(self, realPath:Path):
            self._path = realPath
        def path(self, *args) -> Path:
            rtn = Path(self._path)
            for arg in args:
                if not arg is None: rtn = Path(rtn / Path(arg)).resolve()
            if not rtn.exists(): rtn.mkdir(parents=True, exist_ok=True)
            return rtn 
        def __repr__(self) -> str:
            return str(self._path.resolve())
    ########

    def __init__(self, refPath:Path, logger:object, events:object):
        if refPath == '': refPath = Path(__file__)
        self.log = logger
        self.log.info('sjpath class instantiated')  
        self.event = events
        self.event.add_handler('yaml.load', self.loadYaml)
        self.event.add_handler('yaml.save', self.saveYaml)
        self.reload(refPath=refPath)

    def reload(self, refPath:Path) -> None:
        self.log.info(f'sjPath.reload started with relative path seed: {refPath}')

        self.log.info('Examine all children of refPath, and determine if "appcode" exists as child')
        if Path(refPath / Path('appcode')).exists():
            self.approot = self.sjpathroot(Path(refPath).resolve())
            self.appcode = self.sjpathroot(Path(refPath / "appcode").resolve())
            self.configs = self.sjpathroot(Path(refPath / 'configs').resolve())
            self.orgs    = self.sjpathroot(Path(refPath / 'configs' / 'organizations').resolve())
            self.history = self.sjpathroot(Path(refPath / 'history').resolve())
            self.appname = self.approot.path().name
            self.log.info('appcode found in children, all other paths assigned relative.  AppName is %s' %self.appname)
            return None 

        self.log.info('"appcode" not in children, walk up the path to determine if "appcode" exists as an ancestor')
        for p in Path(refPath).parents:
            if p.name == 'appcode':
                self.approot = self.sjpathroot(p.parent.resolve())
                self.appcode = self.sjpathroot(p.resolve())
                self.configs = self.sjpathroot(Path(p.parent / 'configs').resolve())
                self.orgs    = self.sjpathroot(Path(p.parent / 'configs' / 'organizations').resolve())
                self.history = self.sjpathroot(Path(p.parent / 'history').resolve())
                self.appname = self.approot.path().name
                self.log.info('"appcode" found as ancestor, all other paths assigned relative to that point.  AppName is %s' %self.appname)
                return None 
                
        # If nothing was recognizable as a child nor a parent, then just error with a (hopefuly) helpful message:
        msg = """Reference path supplied does not appear to be structured to support the application, nor matches any expected pattern.
        Perhaps try re-running the installer, or reconcile the starting application path.  Fully qualified path submitted to the application was:
        %s""" %refPath.resolve()
        self.log.error(msg)
        raise FileNotFoundError(msg)
        

    def getDirs(self, filepath:Path) -> dict:
        rtn = {}
        if filepath.is_file:  filepath = Path(filepath.resolve().parent)
        for subdir in [f for f in filepath.iterdir() if f.is_dir()]:
            rtn[subdir.name] = Path(filepath / subdir)
        return rtn 
        

    def getFiles(self, filepath:Path) -> dict:
        rtn = {}
        if filepath.is_file:  filepath = Path(filepath.resolve().parent)
        for file in [f for f in filepath.iterdir() if f.is_file() and f.name[:1] !='.' ]:
            rtn[file.name] = Path(filepath / file)
        return rtn 


    def getFileText(self, filepath:Path) -> str:
        ext = filepath.suffix.upper()
        self.log.debug(f'loading {ext} file into memory string from location: {filepath}')
        if not filepath.exists() or filepath.stat().st_size == 0:
            self.log.error(f'file does not exist or is zero-bytes, aborting and returning "None" (null)')
            return None
        with open(filepath, 'r') as fh:
            rtntext = fh.read()
        self.log.debug(f'file contents loaded into memory with {len(rtntext)} characters')
        return rtntext

    def saveYaml(self, filepath:Path, yamldict:dict):
        self.log.info(f'saving config yaml file: {filepath}')
        self.log.info(f'config yaml file saved:  {filepath}')

    def loadYaml(self, filepath:Path, defaults:dict={}) -> dict:
        self.log.info(f'loading YAML file: {filepath}')
        yamltext = self.getFileText(filepath)
        self.log.info(f'processing yaml into dictionaries')
        try:
            yamldict = yaml.safe_load(yamltext)
        except Exception as ex:
            self.log.error(f'translation from yaml to dictionary failed (perhaps yaml is malformed?), returning empty dictionary')
            self.log.error(f'error message: {ex}')
            self.event.broadcast()
            return defaults

        if len(defaults) >0: 
            self.log.debug(f'applying defaults')
            for n,v in defaults.items():
                if n not in yamldict:
                    yamldict[n] = v

        return yamldict


    def __str__(self):
        msg = []
        msg.append('   approot: %s' %self.approot.path() )
        msg.append('   appcode: %s' %self.appcode.path() )
        msg.append('   history: %s' %self.history.path() )
        msg.append('   configs: %s' %self.configs.path() )
        msg.append('      orgs: %s' %self.orgs.path() )
        self.log.info(f'current paths defined for appname: {self.appname}')
        for m in msg:
            self.log.info(m)
        return '\n'.join(msg)
             
        




if __name__ == '__main__':
    from sjuLog import sjuLog
    log = sjuLog('test-sjpath')
    log.create_stream_handler()
    log.debug('Logging started')
    log.info('Setting Up sjpath test')

    paths = sjuPath(__file__, log)
    print(paths.appname)
    print(paths.approot)
    print(paths.appcode)
    print(paths.history)
    print(paths.configs)
    print(paths.configs.path())
    print(str(paths.configs.path()))
    print(str(paths.configs.path('Teradata','jobs')))

    str(paths)


