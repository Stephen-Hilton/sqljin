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

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject  
import objects.sj_orgs     as sjorg




class sj_ObjectFactory():
    orgs: dict = {}
    log: sjlog.sj_Logger
    paths: sjpaths.sj_Paths
    event: sjevent.sj_Event
    dbconn: dbConnSQLite.dbConn_SQLite

    def __init__(self, utils) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.utils = utils
        self.orgs = {}
        self.log.debug('Object Factory Instantiated')

    # Organizations
    def add_org(self):
        pass 

    def get_org(self):
        pass

    def get_orgs(self):
        pass


    # Systems
    def add_system(self):
        pass 

    def get_system(self):
        pass

    def get_systems(self):
        pass


    # Credentials
    def add_cred(self):
        pass 

    def get_cred(self):
        pass

    def get_creds(self):
        pass


    # Collections
    def add_collection(self):
        pass 

    def get_collection(self):
        pass

    def get_collections(self):
        pass


    # Jobs
    def add_job(self):
        pass 

    def get_job(self):
        pass

    def get_jobs(self):
        pass


    # Steps
    def add_step(self):
        pass 

    def get_step(self):
        pass

    def get_steps(self):
        pass







class sj_OrgFactory():
    orgs: dict = {}
    log: sjlog.sj_Logger
    paths: sjpaths.sj_Paths
    event: sjevent.sj_Event
    dbconn: dbConnSQLite.dbConn_SQLite

    def __init__(self, utils) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.utils = utils
        self.orgs = {}
        self.log.debug('Organization Factory Instantiated')

        # add events handled:
        self.event.add_handler("org.new"       , self.new_organization)
        self.event.add_handler("org.load"      , self.load_organization)
        self.event.add_handler("orgs.load.allinfolder" , self.load_all_organizations_in_folder) 
        # reacting to events:
        self.event.add_handler("app.started" , self.load_all_organizations_in_folder) 
        self.event.add_handler("user.request.new.org" , self.new_organization) 
        self.event.add_handler("test.request.new.org" , self.new_organization) 
        # add to orgs:
        # self.event.add_handler("user.request.refresh.orgs" , 
        


    def load_all_organizations_in_folder(self, folderpath:Path=None):
        if folderpath is None: folderpath = self.paths.configPath.resolve()
        self.log.info(f'preparing to load all Oranizations in folder: {str(folderpath.resolve())}')
        for fo in folderpath.glob('*/'):
            configdb = Path(fo.joinpath('config.db'))
            if configdb.exists():
                self.load_organization(fo.name, configdb)
            else:
                self.log.error(f'invalid path / file not found: {configdb}')
                

    def load_organization(self, orgname:str, create_if_missing:bool=False, datamgr:object = None ) :
        orgpath = Path(self.paths.configPath.resolve() / orgname ).resolve()
        configpath = Path(orgpath / 'config.db').resolve()
        self.log.header(f'loading organization: {orgname}')

        if orgpath.exists() and configpath.exists():
            self.log.debug(f'organization {orgname} folder found: {orgpath}')
            neworg = sj_Org(self.utils, orgname)

        elif create_if_missing:
            self.log.warning(f'folder and/or config.db is missing, creating new...')
            neworg = self.new_organization(orgname)

        else:
            self.log.error(f'config.db is missing for this directory, failing Org load: {orgname}')
            return None 

        if datamgr is None: datamgr = sjdatamgr.sj_DataMgr(self.utils, orgname)
        datamgr.add_handlers()
        datamgr.connect()
        neworg.datamgr = datamgr 
        neworg.load()
        if neworg.name == 'Local': neworg.local = True 
        self.orgs[orgname] = neworg
        return neworg


    def new_organization(self, orgname:str) -> sj_Org:
        orgpath = Path(self.paths.configPath.resolve() / orgname ).resolve()
        datamgr = sjdatamgr.sj_DataMgr(self.utils, orgname)

        if datamgr.configdb_filepath.exists():
            self.log.error(f'new organization requested, but one already exists with that name: {orgname} - ignoring request')
            return None ## 

        else:
            self.log.header(f'creating a new organization: {orgname}')

            # create folder / file structures
            self.log.info(f'creating new structures at path: {orgpath}')
            Path(orgpath / 'plugins' / 'dbConnections').mkdir(parents=True, exist_ok=True)
            Path(orgpath / 'plugins' / 'StepFunctions').mkdir(parents=True, exist_ok=True)
            Path(orgpath / 'plugins' / 'Steps').mkdir(parents=True, exist_ok=True)
            Path(orgpath / 'plugins' / 'Icons').mkdir(parents=True, exist_ok=True)
            
            # create config.db
            self.log.info(f'creating new config.db')
            datamgr.configdb_filepath.touch(exist_ok=True)
            datamgr.connect()

            # setup config.db with correct structures
            sqlfile = Path(self.paths.sjobjectPath / 'sj_neworg.sql').resolve()
            with open(sqlfile,'r') as fh:
                sqls = fh.read()
            for sql in sqls.split(';'):
                if sql.strip() != '':
                    datamgr.dbConn.execute(sql, autocommit=True)

            datamgr.dbConn.execute(f"""insert into sjObjects values(1,'Organization', '{orgname}', 1)""")
            datamgr.dbConn.execute(f"""insert into sjProperties (ID, PropName, PropValue, PropType)  values
                (1,'label', '{orgname}', 'str'),
                (1,'version', '{datetime.strftime(datetime.now(), 'v%Y%m%d' )}', 'str'),
                (1,'icons', '{Path(orgpath / 'plugins' / 'Icons')}', 'path'),
                (1,'remote url', 'http://TBD', 'url'),
                (1,'last update', 'never', 'str'),
                (1,'local', '{orgname=='Local'}', 'bool')
                """)

            return self.load_organization(orgname, datamgr = datamgr)

