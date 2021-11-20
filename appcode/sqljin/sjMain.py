from pathlib import Path
from datetime import datetime
import logging, time, random 

from PyQt6 import QtWidgets as qtw 
from PyQt6 import QtCore as qtc 
from PyQt6 import QtTest as qtt 


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
def log_header(msg):
    log.info('='*60)
    log.info(str(msg).upper())
    log.info('='*60)

def log_ui(msg):
    log.info('(ui-log) %s' %msg)
def log_tbd(msg):
    log.warning('(TBD) %s' %msg)

log_header(f'WELCOME TO {appname.upper()}!')

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

def broadcast(eventname:str, *args, **kwargs) -> list:    
    # confirm the event exists as a registered handler:
    if not eventname in handlers:
        log.warning(f'EVENT "{eventname}" was broadcast, but has no handlers / listeners')
        return None

    # has a handler, so log and send the data off to the correct function(s) for execution   
    # if eventname[:3] != 'log': log.debug(f'EVENT "{eventname}" was broadcast and picked up by {len(handlers[eventname])} handlers')
    rtn = []
    for fn in handlers[eventname]:
        rtn.append( fn(*args, **kwargs) )
    return rtn
    

# add handlers so far:
add_handler('print', print )
add_handler('log', log.debug )
add_handler('log.debug', log.debug )
add_handler('log.info', log.info )
add_handler('log.warning', log.warning )
add_handler('log.error', log.error )
add_handler('log.critical', log.critical )
add_handler('log.header', log_header)
add_handler('log.ui.updater', log_ui)
add_handler('log.ui.main', log_ui)
add_handler('log.tbd', log_tbd)


# build core application functions
def verify_org_config(orgName:str) -> Path:
    pth = Path(paths.configPath / orgName / 'extfiles')
    pth.mkdir(parents=True, exist_ok=True)
    pth = Path(paths.configPath / orgName / 'plugins')
    for plg in ['dbConn', 'inJob', 'onJob']:
        Path(paths.configPath / orgName / 'plugins' / plg ).mkdir(parents=True, exist_ok=True)
add_handler('verify.org.location', verify_org_config)
add_handler('malformed.org.location', verify_org_config)
add_handler('new.org.location', verify_org_config)


def get_listof_orgpaths() -> list:
    """iterate thru paths.config and return list of valid organization Paths"""
    broadcast('log.tbd','get_listof_orgpaths -- iterate thru config.path and return list of all Organization Paths')
    rtn = []
    for p in ['Teradata','Wipro','Local','Global']:
        rtn.append( Path(paths.configPath / p) ) 
    return rtn
add_handler('get.all.organization.paths', get_listof_orgpaths)

def get_org(orgName:str, orgPath:Path) -> object:
    """return the orginzation object for the supplied path"""
    broadcast('log.tbd','get_org(%s) - return the organization object for supplied Path' %orgPath)
    ver = 'v1.3' + str(5 + random.randint(-3,3))
    return {'name':orgName, 'localversion':'1'}
add_handler('get.organization',get_org)

def update_org(orgPath:Path) -> object:
    """compare local org version to source, and update if needed"""
    broadcast('log.tbd','update_org: compare org %s version to source, and update if needed' %orgPath.root)
    qtt.QTest.qWait(1200)
    return object
add_handler('update.organization', update_org)

def update_application():
    """download new code elements for the application itself"""
    broadcast('log.tbd','update_application: download new code elements for the application itself')
    qtt.QTest.qWait(2000)
    return None
add_handler('update.application', update_application)

def get_org_source_version(orgPath) -> str:
    broadcast('log.tbd','get organization: %s source version number from remote master' %orgPath.name)
    return 'v1.23b'
add_handler('get.organization.source.version',get_org_source_version)

def get_org_local_version(orgPath) -> str:
    broadcast('log.tbd','get organization: %s local version number' %orgPath.name)
    return 'v1.23a'
add_handler('get.organization.local.version',get_org_local_version)






# ======================================================
# ============== UI: Updater ===========================
# ======================================================
broadcast('log.header','STARTING UPDATER UI')   
from form_updater import Ui_sjUpdater

class ui_sjUpdater(qtw.QMainWindow, Ui_sjUpdater):
    def __init__(self, *args, **kwargs) -> None:
        broadcast('log.debug','initializing class instance')
        super().__init__()
        self.setupUi(self)
    
        self.autoUpdate = bool(kwargs['autoupdate']) if  'autoupdate' in kwargs else True
        self.chkAutoUpdate.setChecked(self.autoUpdate)

        self.autoAppStart = bool(kwargs['autoappstart']) if 'autoappstart' in kwargs else True 
        self.chkAutoApp.setChecked(self.autoAppStart)
        broadcast('log', 'setting AutoUpdate (%s) and AutoAppStart (%s) behaviors' %(str(self.autoUpdate),str(self.autoAppStart)) )
        
        self.updating = False

    def update_start(self):
        """set ui to a state where the update is free to start"""
        self.log('Beginning update of all components...')
        self.btnOpenApp.setEnabled(False)
        self.btnUpdateRun.setEnabled(False)    
        self.updating = True   

    def update_complete(self):
        """set ui to a state where the update has just completed"""
        self.log('Update Complete!')
        self.btnOpenApp.setEnabled(True)
        self.btnUpdateRun.setEnabled(True)
        self.updating = False

    def update_org_start(self, orgName):
        """set ui elements where the org in question is just beginning to update"""
        self.log('Update started:  %s' %orgName)

    def update_org_complete(self, orgName):
        """set ui elements where the org in question has just completed update"""
        self.log('Update complete: %s' %orgName)
        

    def paused(self):
        self.btnOpenApp.setEnabled(True)
        self.btnUpdateRun.setEnabled(True)
        self.chkAutoUpdate.setChecked(False)
        self.chkAutoApp.setChecked(False)
        self.updating = False
        self.log('Update Paused while %i complete' %self.progressBar.value())

    def log(self, logmsg):
        broadcast('log.ui.updater', logmsg)
        self.txtLogs.appendPlainText(logmsg)
        pass 



# Begin the Updater Application
updater_app = qtw.QApplication([])
uiUpdater = ui_sjUpdater(appname=paths.appname, autoupdate=True, autoappstart=True)
uiUpdater.log('Welcome to %s!' %paths.appname)

# PREWORK BEFORE THE APP IS SHOWN
# Tie UI Events to the application engine Event Framework
uiUpdater.btnPause.clicked.connect(uiUpdater.paused)

# collect all the Org information earlier, so I can fill the tblWidget before Show()
uiUpdater.orgs = {}
for orgs in broadcast('get.all.organization.paths'):
    for org in orgs:
        uiUpdater.orgs[org] = broadcast('get.organization', org)
        uiUpdater.update_org_start(org.name)


# WORK AFTER THE APP IS SHOWN
# Do Work you want to show the user:
uiUpdater.show()    
if uiUpdater.autoUpdate: uiUpdater.update_start()


uiUpdater.log('Update the Application Code, if needed')
broadcast('update_application')

# iterate all orgs and call updates
orgs = broadcast('get.all.organization.paths')[0]
for org in orgs:
    uiUpdater.update_org_start(org.name)
    orgLocalVersion = broadcast('get.organization.local.version', org)
    orgSourceVersion = broadcast('get.organization.source.version', org)
    uiUpdater.log('local version is %s, and source version is %s' %(orgLocalVersion,orgSourceVersion))
    if orgLocalVersion == orgSourceVersion:
        uiUpdater.log('local and source versions match, skipping update')
    else:
        uiUpdater.log('versions are out-of-sync, performing update...')
        broadcast('update.organization', org)
    uiUpdater.update_org_complete(org.name)
    


updater_app.exec()  ## execution doesn't continue past here without closing the app










