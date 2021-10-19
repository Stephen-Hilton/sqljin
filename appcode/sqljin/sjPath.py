from pathlib import Path
from dataclasses import dataclass


@dataclass
class sjPath():
    appcode: object
    approot: object
    configs: object
    history: object
    appname: str

    class sjpathroot():
        _path:Path 
        def __init__(self, realPath:Path):
            self._path = realPath
        def path(self, *args) -> Path:
            rtn = Path(self._path)
            for arg in args:
                rtn = Path(rtn / Path(arg)).resolve()
            if not rtn.exists(): rtn.mkdir(parents=True, exist_ok=True)
            return rtn 
        def __repr__(self) -> str:
            return str(self._path.resolve())

    def __init__(self, refPath:Path=''):
        if refPath == '': refPath = Path(__file__)
        self.reload(refPath=refPath)

    def reload(self, refPath:Path) -> None:
        # Examine all children of refPath, and use if appcode exists there somewhere.
        if Path(refPath / Path('appcode')).exists():
            self.approot = self.sjpathroot(Path(refPath).resolve())
            self.appcode = self.sjpathroot(Path(refPath / "appcode").resolve())
            self.configs = self.sjpathroot(Path(refPath / 'configs').resolve())
            self.history = self.sjpathroot(Path(refPath / 'history').resolve())
            self.appname = self.approot.path().name
            return None 

        # Walk up the path to see if "appcode" exists as one of the parents.
        for p in Path(refPath).parents:
            if p.name == 'appcode':
                self.approot = self.sjpathroot(p.parent.resolve())
                self.appcode = self.sjpathroot(p.resolve())
                self.configs = self.sjpathroot(Path(p.parent / 'configs').resolve())
                self.history = self.sjpathroot(Path(p.parent / 'history').resolve())
                self.appname = self.approot.path().name
                return None 
        
        # If nothing was recognizable as a child nor a parent, then just error with a (hopefuly) helpful message:
        raise FileNotFoundError("""Reference path supplied does not appear to be structured to support the application, nor matches any expected pattern.
        Perhaps try re-running the installer, or reconcile the starting application path.  Fully qualified path submitted to the application was:
        %s""" %refPath.resolve())




if __name__ == '__main__':
    paths = sjPath(__file__)
    print(paths.appname)
    print(paths.approot)
    print(paths.appcode)
    print(paths.history)
    print(paths.configs)
    print(paths.configs.path())
    print(str(paths.configs.path()))
    print(str(paths.configs.path('Teradata','jobs')))