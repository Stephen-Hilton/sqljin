from pathlib import Path
from datetime import datetime
import logging


# START APPLICATION... these are the foundational bits needed first:
appstarttime = str(datetime.now().strftime("%Y%m%d-%H%M%S")) 

def find_approot() -> Path:
    refPath = Path(__file__).resolve()
    rootfound = False
    for p in refPath.parents:
        if p.name == 'appcode':
            return Path(p.parent.resolve())
    # at this point, appcode directory never found
    #  TODO: error handling

class appPaths():
    appname:str = ''
    appRoot:Path = Path()
    codePath:Path = Path()
    logPath:Path = Path()
    applogfilePath:Path = Path()
    configPath:Path = Path()
    globalPath:Path = Path()
    localPath:Path = Path()
    historyPath:Path = Path()
    def __init__(self, appRoot:Path):
        self.appname = appRoot.name
        self.appRoot = Path(appRoot)
        self.codePath = Path(self.appRoot / 'appcode')
        self.logPath = Path(self.codePath / 'logs')
        self.applogfilePath = Path(self.logPath / str('%s--%s.txt' %(self.appname, str(datetime.now().strftime("%Y%m%d-%H%M%S"))))) 
        self.configPath = Path(self.codePath /  'sqljin' / 'configs')
        self.globalPath = Path(self.configPath / 'Global')
        self.localPath = Path(self.configPath / 'Local')
        self.historyPath = Path(self.appRoot / 'history')

paths = appPaths(find_approot())
appname = paths.appname

# SETUP LOGGING
log = logging.Logger(appname)
logformatter = logging.Formatter("%(name)s %(asctime)s %(levelname)8s -- %(message)s", "%Y-%m-%d %H:%M:%S")

shandler = logging.StreamHandler()
shandler.setFormatter(logformatter)
shandler.setLevel(logging.DEBUG)
log.addHandler(shandler)

fhandler = logging.FileHandler(paths.applogfilePath)
fhandler.setFormatter(logformatter)
fhandler.setLevel(logging.DEBUG)
log.addHandler(fhandler)

# FINALLY HAVE LOGGING SET-UP, LET'S START LOGGIING
log.info('='*60)
log.info(f'WELCOME TO {appname.upper()}!')
log.info('='*60)


# BUILD EVENT FRAMEWORK
# event convension:  action.type.name  or  action.type.parent.name
# request is current tense, notifications are past tense
#    some examples:
#           update.system.teradata
#           updated.system.teradata
#           load.collection.teradata.metrics
#           loaded.collection.teradata.solutions
#           get.db.global.variables
#           got.db.global.variables
#           updated.system.teradata.variables

handlers = {}

def add_handler(eventname:str, fn):
    if not eventname in handlers:
        handlers[eventname] = []
    handlers[eventname].append(fn)
    log.info('new event handler "%s" registered to listen for event "%s"' %(str(fn.__name__), eventname))

def broadcast(eventname:str, data=None) -> list:    
    # confirm the event exists as a registered handler:
    if not eventname in handlers:
        log.warning(f'EVENT "{eventname}" was broadcast, but has no handlers / listeners')
        return None

    # has a handler, so log and send the data off to the correct function(s) for execution   
    log.debug(f'EVENT "{eventname}" was broadcast and picked up by {len(handlers[eventname])} handlers')
    rtn = []
    for fn in handlers[eventname]:
        rtn.append( fn(data) )
    return rtn
    

# add handlers so far:
add_handler('print', print )
add_handler('log', log.debug )
add_handler('log.debug', log.debug )
add_handler('log.info', log.info )
add_handler('log.warning', log.warning )
add_handler('log.error', log.error )
add_handler('log.critical', log.critical )


def verify_org_config(orgName:str) -> Path:
    pth = Path(paths.configPath / orgName / 'extfiles')
    pth.mkdir(parents=True, exist_ok=True)
    pth = Path(paths.configPath / orgName / 'plugins')
    for plg in ['dbConn', 'inJob', 'onJob']:
        Path(paths.configPath / orgName / 'plugins' / plg ).mkdir(parents=True, exist_ok=True)
add_handler('verify.org.location', verify_org_config)
add_handler('malformed.org.location', verify_org_config)
add_handler('new.org.location', verify_org_config)


# testing:
if __name__ == '__main__':
    
    add_handler('log.test', log.debug )
    add_handler('log.test', log.info )
    add_handler('log.test', log.warning )

    broadcast('print', 'this is a test of event based print')
    broadcast('log.test', 'This event has three handlers, you should see this message thrice.')
    broadcast('log', 'Super Test')
    broadcast('poopypants')
    broadcast('malformed.org.location', 'Deloitte')


    import updater
    uiUpdater = updater.Ui_sjLoader()
    uiUpdater.setupUi()
