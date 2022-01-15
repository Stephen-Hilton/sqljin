# ######################################################
#
# build factory for all config structures
#
# ######################################################

from pathlib import Path

import dbConn.dbconn_sqlite as dbConnSQLite

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject


class sj_Org(sjobject.sj_Object):
    name: str = ''
    configdb_filepath: Path 
    version: str = 'unknown'
     
    event: sjevent.sj_Event
    log: sjlog.sj_Logger
    paths: sjpaths.sj_Paths
    dbConn: dbConnSQLite.dbConn_SQLite 

    systems: list = None 
    creds: list = None 
    collections: list = None 


    def __init__(self, utils:dict, name:str, configdb_filepath:Path) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.name = name 
        self.configdb_filepath = configdb_filepath
        
        # create datamgr 
        self.datamgr = sjdatamgr.sj_DataMgr(self)


    

    def connect_configdb(self):
        self.dbConn = dbConnSQLite.dbConn_SQLite(self.log, systemname=f'app specific ({self.paths.appname}) SQLite', host=self.configdb_filepath)
        self.dbConn.connect()
        self.dbConn.autocommit_default = True
        

    def load(self):
        self.log.info(f'loading config for {self.name}')
        self.log.debug(f'configdb located at: {self.configdb_filepath}')
        # connect to the app_dbConn version of sqlite driver
        self.connect_configdb()
        
        # build child objects
        self.systems = self.load_systems()
        self.creds = self.load_creds()
        self.collections = self.load_collections()

        self.log.info(f'config {self.name} fully loaded')


    def load_systems(self) -> list:
        self.log.info(f'loading all systems into org {self.name}')
        objlist = self._rows_to_objects( self.datamgr.get_objects_data('System') )
        objlist = self._sort_objects(objlist)
        # TODO

    def load_creds(self) -> list:
        if self.name == 'Local':
            self.log.info(f'loading all credentials into org {self.name}')
            objlist = self._rows_to_objects( self.datamgr.get_objects_data('Credential') )
            objlist = self._sort_objects(objlist)
        # TODO

    def load_collections(self) -> list:
        self.log.info(f'loading all collections into org {self.name}')
        objlist = self._rows_to_objects( self.datamgr.get_objects_data('Collection') )
        for collection in objlist:
            pass  # call get_jobs()
        objlist = self._sort_objects(objlist)
        # TODO



    def _sort_objects(self, objlist:list) -> list:
        self.log.debug('sorting object list...')
        # TODO
        return objlist

    def _rows_to_objects(self, datalist:list) -> list:
        self.log.debug('translating configDB data into program objects')
        objlist = []
        # TODO
        return objlist







    # OBJECT OPERATIONS:
    def new_object(self, objecttype:str, instancename:str, active:bool = True):
        self.log.info(f"inserting a new '{objecttype}' called '{instancename}' in organization '{self.name}'")
        # SQLite should auto-increment the ID, as it's an INT PRIMARY KEY and therefore an alias for RowID
        self.dbConn.execute(f"""Insert into sjObjects (ObjectType, InstanceName, Active) VALUES ('{objecttype}' ,'{instancename}', {1 if active else -1})""")


    def get_objects(self, ids:list=[], objecttypes:list=[], instancenames:list=[], active_only:bool=True, include_properties:bool=True):
        # build sql for getting correct data from DB
        whereids   = f" ID in ({','.join([str(i) for i in ids]) }) " if ids != [] else ''
        whereobj   = f" ObjectType in(%s) " %','.join([f"'{o}'" for o in objecttypes]) if objecttypes !=[] else ''
        whereinst  = f" InstanceNames in(%s) " %','.join([f"'{i}'" for i in instancenames]) if instancenames !=[] else ''
        whereactive= f" Active > 0 " if active_only else ''
        wheres = [w for w in [whereids, whereobj, whereinst, whereactive] if w != '']
        self.log.debug(f"get all objects in organization '{self.name}' where {'and'.join(wheres)}")
        listofobjects = self.dbConn.execute(f"""
            select * from {'ObjProp' if include_properties else 'Objects'}
            where {'and'.join(wheres) }
            order by {'ObjectType, InstanceName, Sort, PropName' if include_properties else 'ObjectType, InstanceName'}
            """, 'list')[1]

        rtnobjects = []

        if include_properties:  # separate the returned list into object and property objects
            idsfound = []
            rtn = []
            newobj = {}

            # loop thru all list of objects
            for i, objdict in enumerate(listofobjects):  
                # if we're starting a new ID
                if objdict['id'] not in idsfound: 
                    idsfound.append(objdict['id'])

                    # save previous Id if exists
                    if newobj != {}: rtn.append(newobj)

                    # next, build our new singular object dict
                    newobj = {  'id':objdict['id'], 
                                'objecttype':objdict['objecttype'],
                                'instancename':objdict['instancename'],
                                'active':objdict['active'],
                                'properties': [] }

                # every row, append (valid) properties to the newobj
                if objdict['property'] is not None:
                    newobj['properties'].append( {  'id'           :objdict['id'],
                                                    'propname'     :objdict['propname'], 
                                                    'propvalue'        :objdict['propvalue'],
                                                    'proptype'     :objdict['proptype'],
                                                    'sort'         :objdict['sort'],
                                                    'variableflag' :objdict['variableflag'],
                                                    'startts'      :objdict['startts'] })
                
                # finally, make sure we aren't off-by-one and leave out our last object:
                if i == len(listofobjects)-1: rtn.append(newobj)

        return rtn

    def expire_object(self, id:int):
        self.log.info(f"expiring an object (id = '{id}') for organization '{self.name}'")
        self.dbConn.execute(f"""update sjObjects set Active = -(abs(Active)+1) where ID = {id}""")

    def restore_object(self, id:int):
        self.log.info(f"restoring (making active) an object with id = '{id}' for organization '{self.name}'")
        self.dbConn.execute(f"""update sjObjects set Active = abs(Active)+1 where ID = {id}""")
  
    def expire_property(self, id:int, property:str):
        self.set_property(id, property, '***deleted***')
        return None

    def restore_property(self, id:int, property:str):
        self.set_property(id, property)
        return None

    def _objprop_objectify(self, objprop:list) -> list:
        idsfound = []
        rtn = []
        newobj = {}

        # loop thru all list-of-dict / objects
        for i, objdict in enumerate(objprop):  

            # if we're starting a new ID
            if objdict['id'] not in idsfound: 
                idsfound.append(objdict['id'])

                # save previous Id if exists
                if newobj != {}: rtn.append(newobj)

                # next, build our new singular object dict
                newobj = {  'id':objdict['id'], 
                            'objecttype':objdict['objecttype'],
                            'instancename':objdict['instancename'],
                            'active':objdict['active'],
                            'properties': [] }

            # every row, append (valid) properties to the newobj
            if objdict['property'] is not None:
                newobj['properties'].append( {  'id'           :objdict['id'],
                                                'propname'     :objdict['propname'], 
                                                'propvalue'    :objdict['propvalue'],
                                                'proptype'     :objdict['proptype'],
                                                'sort'         :objdict['sort'],
                                                'varflag'      :objdict['varflag'],
                                                'startts'      :objdict['startts'] })
            
            # finally, make sure we aren't off-by-one and leave out our last object:
            if i == len(objprop): rtn.append(newobj)






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

    def load_organization(self, name:str, configdb_filepath:Path ):
        self.log.header(f'loading organization: {name}')
        self.log.debug(f'organization {name} configdb filepath: {configdb_filepath}')
        neworg = sj_Org(self.utils, name, configdb_filepath)
        isunique = True
        if not isunique:
            self.log.error(f'the organization {name} has a redundant orgid with an existing org')
            self.log.error(f'until an automated process is built, you will have to ensure unique orgid manually')
            #TODO: automate deduplication of OrgIDs
            neworg = None 
            return None 
        self.orgs[name] = neworg

        return neworg

    def new_organization(self, name:str) -> sj_Org:
        newpath = Path(self.paths.configPath / name)
        self.log.header(f'creating a new organization: {name}')
        self.log.info(f'creating new structures at path: {newpath}')

        Path(newpath / 'plugins' / 'dbConnections').mkdir(parents=True, exist_ok=True)
        Path(newpath / 'plugins' / 'StepFunctions').mkdir(parents=True, exist_ok=True)
        Path(newpath / 'plugins' / 'Steps').mkdir(parents=True, exist_ok=True)
        Path(newpath / 'plugins' / 'Icons').mkdir(parents=True, exist_ok=True)
        
        newconfigdb = Path(newpath / 'config.db')
        self.log.info('creating config database at: %s' %newconfigdb )
        newconfigdb.touch(exist_ok=True) 

        neworg = self.load_organization(name, newconfigdb)
        neworg.connect_configdb()

        sqlfile = Path(self.paths.sjobjectPath / 'sj_neworg.sql').resolve()
        self.log.info(f'constructing required database structures from file: {sqlfile}')
        with open(sqlfile,'r') as fh:
            sqls = fh.read()
        for sql in sqls.split(';'):
            if sql.strip() != '':
                neworg.dbConn.execute(sql)
        return neworg

