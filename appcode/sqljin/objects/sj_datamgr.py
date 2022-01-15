# ######################################################
#
# Data Manager for all object traffic to/from dbConnection
#
# ######################################################

from pathlib import Path

import dbConn.dbconn_sqlite as dbConnSQLite

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths

import objects.sj_orgs     as sjorg  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject  

class sj_DataMgr():
    """ 
    DataMgr manages all data work to/from the configdb, including getting/setting/creating/expiring
    all objects and properties.  It is intended to be a singular object per Organization, created by 
    the Org object, as that is the level each ConfigDB is aligned to.  The DataMgr is then made 
    available thru the event framework. The event framework also enables cross-Org data work.
    """
    dbConn: dbConnSQLite.dbConn_SQLite = None
    log: sjlog.sj_Logger
    event: sjevent.sj_Event
    paths: sjpaths.sj_Paths
    parentOrg: sjorg.sj_Org
    configdb_filepath: Path

    def __init__(self, parentOrg:sjorg.sj_Org, load:bool=True) -> None:
        self.event = parentOrg.event
        self.log   = parentOrg.log
        self.paths = parentOrg.paths
        self.parentOrg = parentOrg
        self.event_prefix = f'{parentOrg.name}.datamgr.'
        self.configdb_filepath = parentOrg.configdb_filepath.resolve()
        self.connect()
        


    def connect(self) -> bool:
        if self.dbConn is None or not self.dbConn.connected(): 
            self.dbConn = dbConnSQLite.dbConn_SQLite(self.log, systemname=f'app specific ({self.paths.appname}) SQLite', host=self.configdb_filepath)
        self.dbConn.autocommit_default = True
        self.event.broadcast(f'{self.event_prefix}.CONNECTED', datamgr = self)
        return self.dbConn.connected()

    def disconnect(self) -> bool:
        if self.dbConn.connected(): self.dbConn.disconnect()
        self.event.broadcast(f'{self.event_prefix}.DISCONNECTED', datamgr = self)
        return not self.dbConn.connected()



    # OBJECT MANAGEMENT:  functions that are passed into sjObject / sjProperty objects at create time
    def save_properties(self, props:list) -> bool:
        self.log.info(f"saving properties:") 
        updatelines = []
        success = True
        for prop in props:
            if type(prop) is sjprop.sj_Property:
                self.log.info(f"  {prop.parentOrg.name}.{prop.parentObject.objecttype}.{prop.parentObject.instancename}.{prop.propname}") 
                updatelines.append("({prop.id}, '{prop.propname}', '{prop.propvalue}', '{prop.proptype}', '{prop.sort}', '{prop.varflag}')")
            else:
                self.log.error(f"!!save_properties was passed an object that wasn't a property type: {type(prop)}")
                self.log.error(f"!!skipping this save operation")
                success = False        
        rtn = self.dbConn.execute(f"""
            insert into sjProperties (ID, PropName, PropValue, PropType, Sort, VarFlag)
            VALUES {','.join(updatelines)} 
            """, datareturned='none' )
        if rtn is None: 
            self.log.error('failed to save any Properties! Blah!!!')
            return False
        else:
            return success

    def save_property(self, prop:sjprop.sj_Property) -> bool:
        return self.save_properties([prop])


    def get_objects_data(self, objtype:str, historic:bool = False) -> list:
        self.log.info(f'getting all object data for object type: {objtype}')
        tbl = 'ObjProp_History' if historic else 'ObjProp'
        rtn = self.dbConn.execute(f"""
            select * from {tbl} 
            where {self.get_where(objtype=objtype)}
            order by ObjectType, InstanceName, Sort
            """, datareturned='list')
        return rtn





    def get_objects(self, **kwargs) -> list:
        self.log.debug(f"retrieving objects from '{self.orgname}' data manager")
        rtn = self.dbConn.execute(f'Select * from ObjProp_History where {self.get_where(kwargs)}','list')
        rows = rtn["data"]

        # TODO: process rows into objects / property, then return list of objects
        pass 



    def expire_object(self, obj:sjobject.sj_Object):
        self.log.info(f"expiring an object('{obj.id}'): {obj.parentOrg.name}.{obj.objecttype}.{obj.instancename}")
        self.dbConn.execute(f"""update sjObjects set Active = -(abs(Active)+1) where ID = {obj.id}""")

    def restore_object(self, obj:sjobject.sj_Object):
        self.log.info(f"restoring an object('{obj.id}'): {obj.parentOrg.name}.{obj.objecttype}.{obj.instancename}")
        self.dbConn.execute(f"""update sjObjects set Active = abs(Active)+1 where ID = {obj.id}""")
  

    def get_proptype_from_pytype(self, pytype) -> str:
        if   type(pytype) is int:   return 'int'
        elif type(pytype) is float: return 'float'
        elif type(pytype) is str:   return 'str'
        

    def get_where(self, **kwargs) -> str:
        id = objtypes = instname = propnames = propvalues = proptypes = sort = []
        varflag = historic = deleted = onlyobject = onlyproperty = False
        for n, v in kwargs:
            if n in ['id','ids']:
                ids = kwargs[n]
                if type(ids) is not list: ids = [ ids ]
            if n in ['object','objects','objecttype','objecttypes']:
                objtypes = kwargs[n]
                if type(objtypes) is not list: objtypes = [ objtypes ]
            if n in ['instance','instances','instancename','instancenames']:
                instname = kwargs[n]
                if type(instname) is not list: instname = [ instname ]
            if n in ['name','names','propname','propnames']:
                propnames = kwargs[n]
                if type(propnames) is not list: propnames = [ propnames ]
            if n in ['value','values','propvalue','propvalues']:
                propvalues = kwargs[n]
                if type(propvalues) is not list: propvalues = [ propvalues ]
            if n in ['type','types','proptype','proptypes']:
                proptype = kwargs[n]
                if type(proptype) is not list: proptype = [ proptype ]
            if n in ['sort']:
                sort = kwargs[n]
                if type(sort) is not list: sort = [ sort ]
            if n in ['varflag','variable','variables','only_varflag']:
                varflag = bool(kwargs[n])
            if n in ['historic','include_historic']:
                historic = bool(kwargs[n])
            if n in ['deleted','include_deleted', 'show_deleted']:
                deleted = bool(kwargs[n])
            if n in ['just_object', 'object_only','only_obj', 'object_only','exclude_properties']:
                object_only =  bool(kwargs[n])
            if n in ['just_property','only_property','only_prop', 'exclude_object','exclude_objects']:
                exclude_object = bool(kwargs[n])


        whereids     = f" ID in({','.join(ids)}) " if ids !=[] else ''
        whereobjtype = f" ObjectType in(%s) " %','.join([f"'{o}'" for o in objtypes]) if objtypes !=[] and not exclude_object else ''
        whereoinst   = f" InstanceName in(%s) " %','.join([f"'{o}'" for o in instname]) if instname !=[] and not exclude_object else ''
        wherepname   = f" PropName in(%s) " %','.join([f"'{p}'" for p in propnames]) if propnames !=[]  and not object_only else ''
        wherepval    = f" PropValue in(%s) " %','.join([f"'{p}'" for p in propvalues]) if propvalues !=[] and not object_only else ''
        whereptype   = f" PropType in(%s) " %','.join([f"'{d}'" for d in proptype])  if proptype !=[] and not object_only  else ''
        wheresort    = f" Sort in({','.join(sort)}) " if sort !=[] and not object_only else ''
        wheredel     = f" PropValue != '***deleted***' " if not deleted and not object_only else ''
        wherevar     = f" VarFlag != 0" if varflag and not object_only else '' 
        wherehist    = '' if historic or object_only else """(ID, PropName, StartTS) in 
        (Select ID, PropName, max(StartTS) from sjProperties group by ID, PropName)"""
        wheres = [w for w in [whereids, wherepname, wherepval, whereptype, wheresort, wheredel, wherevar, wherehist] if w != '']
        return str('and'.join(wheres))




class sj_DataMgr_Factory():
    dbConn: dbConnSQLite.dbConn_SQLite
    log: sjlog.sj_Logger
    event: sjevent.sj_Event
    paths: sjpaths.sj_Paths

    def __init__(self, utils:dict) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.utils = utils 

    def new_datamgr(self, orgname:str, configdb_filepath:Path) -> sj_DataMgr:
        dbconn = self.dbConn.connect(host = configdb_filepath.resolve())
        return sj_DataMgr(orgname, configdb_filepath, self.dbConn)


if __name__ == '__main__':
    print('test run')