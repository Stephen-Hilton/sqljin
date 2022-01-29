# ######################################################
#
# Organization and Org Factory structures
#
# ######################################################

from pathlib import Path
from datetime import datetime

import dbConn.dbconn_sqlite as dbConnSQLite

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_object   as sjobject


class sj_Org(sjobject.sj_Object):
    name: str = ''
    configdb_filepath: Path 

    systems: list = None 
    creds: list = None 
    collections: list = None 


    def __init__(self, utils:dict, orgname:str) -> None:
        self.name = orgname 
        self.id = 1
        super().__init__(utils, self, loadcriteria=None) 
    

    def load(self):
        super().load()
        
        # build child objects
        self.systems = self.load_systems()
        self.creds = self.load_creds()
        self.collections = self.load_collections()
        self.log.info(f'oranization {self.name} fully loaded with all direct children')
        self.log.line()

    # Systems
    def new_system(self):
        pass 

    def load_systems(self) -> list:
        self.log.info(f'loading all systems into org {self.name}')
        #objlist = self.event.broadcast(f"{self.orgname}.datamgr.load.id", self.id )

        # TODO

    def load_creds(self) -> list:
        self.log.info(f"loading all system credenitals into org {self.name}")
        # TODO

    def load_collections(self) -> list:
        self.log.info(f'loading all collections into org {self.name}')
        # TODO







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


    def load_all_organizations_in_folder(self, folderpath:Path):
        self.log.info(f'preparing to load all Oranizations in folder: {str(folderpath.resolve())}')
        for fo in folderpath.glob('*/'):
            configdb = Path(fo.joinpath('config.db'))
            if configdb.exists():
                self.load_organization(fo.name, configdb)
            else:
                self.log.error(f'invalid path / file not found: {configdb}')
                

    def load_organization(self, orgname:str, create_if_missing:bool=False, datamgr:object = None ) -> sj_Org:
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

