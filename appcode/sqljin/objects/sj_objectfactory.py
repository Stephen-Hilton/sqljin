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
import objects.sj_orgs     as sjorg




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

    # Organizations
    def add_org(self):
        pass 

    def load_org(self, orgname:str, create_ifmissing:bool=False):
        # create datamgr for the organization, based on folder path of the config.db file
        datamgr = sjdatamgr.sj_DataMgr(self.utils, orgname)
        pass

    def load_orgs(self, create_ifmissing:bool=False):
        pass

    def load_orgs_in_configpath(self, configpath:Path=None):
        if not configpath: configpath = self.paths.configPath
        pass



    # Systems
    def add_system(self):
        pass 

    def load_system(self, create_ifmissing:bool=False):
        pass

    def load_systems(self, create_ifmissing:bool=False):
        pass


    # Credentials
    def add_cred(self):
        pass 

    def load_cred(self, create_ifmissing:bool=False):
        pass

    def load_creds(self, create_ifmissing:bool=False):
        pass


    # Collections
    def add_collection(self):
        pass 

    def load_collection(self, create_ifmissing:bool=False):
        pass

    def load_collections(self, create_ifmissing:bool=False):
        pass


    # Jobs
    def add_job(self):
        pass 

    def load_job(self, create_ifmissing:bool=False):
        pass

    def load_jobs(self, create_ifmissing:bool=False):
        pass


    # Steps
    def add_step(self):
        pass 

    def load_step(self, create_ifmissing:bool=False):
        pass

    def load_steps(self, create_ifmissing:bool=False):
        pass




