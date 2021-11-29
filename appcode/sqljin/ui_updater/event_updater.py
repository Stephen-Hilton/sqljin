
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



