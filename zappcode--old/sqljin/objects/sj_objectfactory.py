# ######################################################
#
# Object Factory - create / load various object types
#
# ######################################################

from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

import dbConn.dbconn_sqlite as dbConnSQLite

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths
import util.sj_misc   as sjmisc

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject  
import objects.sj_org     as sjorg



class sj_ObjectFactory():
    orgs: dict = {}
    log: sjlog.sj_Logger
    paths: sjpaths.sj_Paths
    event: sjevent.sj_Event
    misc:  sjmisc.sj_Misc
    dbconn: dbConnSQLite.dbConn_SQLite

    def __init__(self, utils) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.misc  = utils['misc']
        self.utils = utils
        self.orgs = {}
        self.log.debug('Object Factory Instantiated')
        self.logtext_add = 'add_{1} called, to create a new {2} from scratch for {3}'

    
    # --------------------------------------------
    # Organizations
    # --------------------------------------------
    def add_org(self, orgname:str):
        self.log.info(f'add_org called for: {orgname}')
        pass 


    def load_org(self, orgname:str, create_ifmissing:bool=False):
        orgpath = Path(self.paths.configPath / orgname)
        self.log.info(f'load_org called, to loading an org from existing config path:\n\t{ str(orgpath.resolve()) }')

        # Testing of required environmental bits:
        if not orgpath.exists and create_ifmissing:
            self.log.warning(f'{ orgname } not found, creating instead (create_ifmissing = True)')
            return self.add_org(orgname)
        elif not orgpath.exists:
            self.log.error(f'Organization Path not found: \n\t{ orgpath.resolve } \n\t')
            # raise FileNotFoundError(f'Org path not found: \n\t{ orgpath.resolve } \n\t')
            return None 

        # ALL IS WELL:
        # create datamgr for the organization, based on folder path of the config.db file
        datamgr = sjdatamgr.sj_DataMgr(self.utils, orgname)
        datamgr.add_handlers()
        datamgr.connect()
        neworg = sjorg.sj_Org(self.utils, orgname) 
        neworg.load()
        neworg.add_handlers()
        return neworg 

    def load_orgs(self, configpath:Path=None, create_ifmissing:bool=False):
        self.log.info(f'load_orgs called, to loading all orgs from config path')
        if not configpath: configpath = self.paths.configPath
        pass


    # --------------------------------------------
    # Systems
    # --------------------------------------------
    # 
    def add_system(self, sysname:str):
        self.log.info(f'add_system called for: {sysname}')
        pass 

    def load_system(self, create_ifmissing:bool=False):
        self.log.info(f'load_system called, to loading an org from config path')
        pass

    def load_systems(self, create_ifmissing:bool=False):
        pass


    # --------------------------------------------
    # Credenials
    # --------------------------------------------
    def add_cred(self, credname:str):
        self.log.info(f'add_cred called for: {credname}')
        pass 

    def load_cred(self, create_ifmissing:bool=False):
        pass

    def load_creds(self, create_ifmissing:bool=False):
        pass


    # --------------------------------------------
    # Collections
    # --------------------------------------------
    def add_collection(self, collname:str):
        self.log.info(f'add_collection called for: {collname}')
        pass 

    def load_collection(self, create_ifmissing:bool=False):
        pass

    def load_collections(self, create_ifmissing:bool=False):
        pass


    # --------------------------------------------
    # Jobs
    # --------------------------------------------
    def add_job(self, jobname:str):
        self.log.info(f'add_job called for: {jobname}')
        pass 

    def load_job(self, create_ifmissing:bool=False):
        pass

    def load_jobs(self, create_ifmissing:bool=False):
        pass


    # --------------------------------------------
    # Steps
    # --------------------------------------------
    def add_step(self, stepname):
        self.log.info(f'add_step called for: {stepname}')
        pass 

    def load_step(self, create_ifmissing:bool=False):
        pass

    def load_steps(self, create_ifmissing:bool=False):
        pass

