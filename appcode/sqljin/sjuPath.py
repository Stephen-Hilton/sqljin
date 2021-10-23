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

    def __init__(self, refPath:Path, logger:object):
        if refPath == '': refPath = Path(__file__)
        self.log = logger
        self.log.info('sjpath class instantiated')  
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
        for subdir in [f for f in filepath.iterdir() if f.is_dir()]:
            rtn[subdir.name] = Path(filepath / subdir)
        return rtn 
        

    def getFiles(self, filepath:Path) -> dict:
        rtn = {}
        for file in [f for f in filepath.iterdir() if f.is_file() and f.name[:1] !='.' ]:
            rtn[file.name] = Path(filepath / file)
        return rtn 


    def getFileText(self, filepath:Path) -> str:
        ext = filepath.suffix.upper()
        self.log.debug(f'opening {ext} file into memory string: {filepath}')
        if not filepath.exists() or filepath.stat().st_size == 0:
            self.log.error(f'file does not exist or is zero-bytes, aborting and returning "None" (null)')
            return None
        with open(filepath, 'r') as fh:
            rtntext = fh.read()
        self.log.debug(f'file contents loaded into memory with {len(rtntext)} characters')
        return rtntext


    def getYaml(self, filepath:Path, defaults:dict={}, constraints:dict={}) -> dict:
        yamltext = self.getFileText(filepath)
        try:
            yamldict = yaml.safe_load(yamltext)
        except Exception as ex:
            self.log.error(f'translation from yaml to dictionary failed (perhaps yaml is malformed?), returning empty dictionary')
            self.log.error(f'error message: {ex}')
            return {}

        if len(defaults) >0:
            self.log.debug(f'applying defaults')
            for k,v in defaults.items():
                if k not in yamldict: yamldict[k] = v

        try:
            constraints = list(constraints)
            if len(constraints) >0:
                self.log.debug(f'applying constraints')
                violations = []
                for k,v in yamldict.items():
                    if k not in constraints:
                        violations.append(k)
                for k in violations:
                    del yamldict[k]
        except Exception as ex:
            self.log.error(f'if supplied, constraint must be a list-like object - aborting and returning empty dictionary')
            return {}
            
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


