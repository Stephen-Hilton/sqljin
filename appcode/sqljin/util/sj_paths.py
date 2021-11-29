from pathlib import Path 
from datetime import datetime 

print(f'loaded {__name__}')

class sj_Paths():
    appname:str = ''
    approotPath:Path = Path()
    codePath:Path = Path()
    applogPath:Path = Path()
    configPath:Path = Path()
    applogfilePath:Path = Path()
    globalPath:Path = Path()
    localPath:Path = Path()
    historyPath:Path = Path()

    def __init__(self, approotPath:Path=''):
        self.appstarttime = str(datetime.now().strftime("%Y%m%d-%H%M%S")) 

        self.approotPath = self.find_approotPath() if approotPath=='' else Path(approotPath) 
        self.appname = self.approotPath.name
        self.codePath = Path(self.approotPath / 'appcode')
        self.applogPath = Path(self.codePath / 'logs')
        self.applogfilePath = Path(self.applogPath / str('%s--%s.txt' %(self.appname, self.appstarttime))) 
        self.configPath = Path(self.approotPath / 'configs')
        self.globalPath = Path(self.configPath / 'Global')
        self.localPath = Path(self.configPath / 'Local')
        self.historyPath = Path(self.approotPath / 'history')

    def find_approotPath(self) -> Path:
        refPath = Path(__file__).resolve()
        rootfound = False
        for p in refPath.parents:
            if p.name == 'appcode':
                return Path(p.parent.resolve())
        # at this point, appcode directory never found
        #  TODO: error handling
