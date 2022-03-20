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

import objects.sj_org     as sjorg   
import objects.sj_object   as sjobject  
import objects.sj_property as sjprop 


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
    configdb_filepath: Path
    orgname:str

    def __init__(self, utils:dict, orgname:str) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.configdb_filepath = Path(self.paths.configPath.resolve() / orgname / 'config.db').resolve()
        self.orgname = orgname 
        self.event_prefix = f'{self.orgname}.datamgr'
        self.log.info(f'starting new data manager for {self.orgname}')
        

    def add_handlers(self):
        self.event.add_handler(f"{self.event_prefix}.load.id", self.load_object_by_id)
        self.event.add_handler(f"{self.event_prefix}.new", self.new_object)
        self.event.add_handler(f"{self.event_prefix}.save", self.save_object)
        self.event.add_handler(f"{self.event_prefix}.expire", self.expire_object)
        self.event.add_handler(f"{self.event_prefix}.restore", self.restore_object)
        self.event.add_handler(f"{self.event_prefix}.get.objects", self.get_objects)

        # old:
        self.event.add_handler(f"{self.event_prefix}.prop.refresh", self.refresh_prop)
        self.event.add_handler(f"{self.event_prefix}.prop.save", self.save_prop)
        self.event.add_handler(f"{self.event_prefix}.props.save", self.save_props)
        self.event.add_handler(f"{self.event_prefix}.prop.save.dict", self.save_prop_from_dict)
        self.event.add_handler(f"{self.event_prefix}.prop.load", self.load_prop)
        self.event.add_handler(f"{self.event_prefix}.prop.load.id_name", self.load_prop_from_id_name)
        self.event.add_handler(f"{self.event_prefix}.prop.delete", self.delete_prop)
        self.event.add_handler(f"{self.event_prefix}.prop.expire", self.delete_prop)
        self.event.add_handler(f"{self.event_prefix}.prop.restore", self.restore_prop)


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



    # --------------------------------
    # --------------------------------
    # Objects:
    # --------------------------------
    # --------------------------------

    def save_object(self, obj:sjobject.sj_Object):
        self.log.debug(f"saving object data ('{obj.id}'): {obj.orgname}.{obj.objecttype}.{obj.instancename}")
        # really, saving an object only means saving all properties
        for prop in obj.props:
            prop.save()

    def load_object_by_id(self, id:int) -> dict:
        self.log.debug(f"retrieving object data by ID ({id}) for organization: {self.orgname}") 
        rtn =  self.dbConn.execute(f"select * from ObjProp where ID = {id}", 'list')
        return rtn

    def expire_object(self, obj:sjobject.sj_Object) -> bool:
        self.log.info(f"expiring an object('{obj.id}'): {obj.parentOrg.name}.{obj.objecttype}.{obj.instancename}")
        self.dbConn.execute(f"""update sjObjects set Active = -(abs(Active)+1) where ID = {obj.id}""")
        rtn = self.load_object_by_id( obj.id )
        return rtn['data'] != {}

    def restore_object(self, obj:sjobject.sj_Object) -> dict:
        self.log.info(f"restoring an object('{obj.id}'): {obj.parentOrg.name}.{obj.objecttype}.{obj.instancename}")
        self.dbConn.execute(f"""update sjObjects set Active = abs(Active)+1 where ID = {obj.id}""")
        return  self.load_object_by_id( obj.id )
        
    def new_object(self, objecttype:str, instancename:str, props:list=[]) -> dict:
        self.log.debug(f"creating new object in organization: {self.orgname}: {objecttype}.{instancename}") 
        rtn = self.dbConn.execute(f"""
            insert into sjObjects (ID, ObjectType, InstanceName) 
            select max(id)+1 as ID
            ,'{ objecttype.replace("'","''") }' as ObjectType
            ,'{ instancename.replace("'","''") }' as InstanceName
            from sjObjects """, 'list')
        self.save_props(props)
        return rtn



    # --------------------------------
    # --------------------------------
    # Properties:
    # --------------------------------
    # --------------------------------

    def save_prop(self, prop:sjprop.sj_Property):
        self.log.debug(f"saving property ('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        self.save_prop_from_dict({'id':prop.id, 'propname':prop.propname, 'propvalue':prop.propvalue, 'proptype':prop.proptype, 'sort':prop.sort, 'varflag':prop.varflag} )
        rtn = self.refresh_prop(prop)
        return rtn  

    def save_props(self, props:list):
        """saves a list of dicts containing property data"""
        if props != []:
            values = []
            for prop in props:
                id = prop['id'] 
                propname = str(prop['propname']).replace("'","''")
                propvalue = str(prop['propvalue']).replace("'","''") if 'propvalue' in prop else '' 
                proptype = prop['proptype'] if 'proptype' in prop else 'str'
                values.append(f"( {id}, '{propname}', '{propvalue}', '{proptype}')")

            allvalues = ', \n'.join(values) 
            self.dbConn.execute(f"""insert into sjProperties (ID, PropName, PropValue, PropType)  values
            {allvalues} """)
  


    def save_prop_from_dict(self, prop:dict):
        self.log.debug(f"saving property (dict version): {self.orgname}('{prop['id']}') {prop.propname} = {prop.propname}")
        self.dbConn.execute(f"""insert into sjProperties (ID, PropName, PropValue, Proptype, Sort, VarFlag) 
        values ({prop['id']}, '{prop['propname']}', '{prop['propvalue']}', '{prop['proptype']}', {prop['sort']}, {prop['varflag']} ) """)
        rtn = self.refresh_prop(prop)
        return rtn  

    def load_prop_from_id_name(self, id:int, propname:str):
        self.log.info(f"loading property from config.db, for object: {self.orgname}.ID={id}.PropName={propname}")
        rtn = self.dbConn.execute(f"""select * from Properties where ID = {id} and PropName = '{propname}' """, 'list')
        return rtn 

    def load_prop(self, prop:sjprop.sj_Property):
        return self.load_prop_from_id_name( prop.id, prop.propname )

    def refresh_prop(self, prop:sjprop.sj_Property):
        return self.load_prop_from_id_name( prop.id, prop.propname )

    def delete_prop(self, prop:sjprop.sj_Property) -> bool:
        self.log.info(f"expiring (soft delete) property ('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        self.save_prop_from_dict({'id':prop.id, 'propname':prop.propname, 'propvalue':'***deleted***', 'proptype':prop.proptype, 'sort':prop.sort, 'varflag':prop.varflag} )
        rtn = self.refresh_prop(prop)
        prop.parentobject.allprops_remove_deleted()
        return rtn['data'] == {}

    def restore_prop(self, prop:sjprop.sj_Property, asoftime:str):
        pass # TBD if needed




    ### function for getting many objects at once (used by Org, not Objects/Properties)
    def get_objects(self, **kwargs) -> list:
        self.log.debug(f"retrieving multiple objects (data) from '{self.orgname}' data manager")
        where = self.get_where(**kwargs)
        rtn = self.dbConn.execute(f'Select * from ObjProp where {where} order by ObjectType, InstanceName, ID, Sort', 'list')
        return rtn



    def get_where(self, **kwargs) -> str:
        ids = objtypes = instname = propnames = propvalues = proptypes = sort = []
        varflag = historic = deleted = object_only = prop_only = False
        for n, v in kwargs.items():
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

        whereids     = f" ID in({','.join(ids)}) " if ids !=[] else ''
        whereobjtype = f" ObjectType in(%s) " %','.join([f"'{o}'" for o in objtypes]) if objtypes !=[]  else ''
        whereoinst   = f" InstanceName in(%s) " %','.join([f"'{o}'" for o in instname]) if instname !=[]  else ''
        wherepname   = f" PropName in(%s) " %','.join([f"'{p}'" for p in propnames]) if propnames !=[]   else ''
        wherepval    = f" PropValue in(%s) " %','.join([f"'{p}'" for p in propvalues]) if propvalues !=[]  else ''
        whereptype   = f" PropType in(%s) " %','.join([f"'{d}'" for d in proptypes])  if proptypes !=[]   else ''
        wheresort    = f" Sort in({','.join(sort)}) " if sort !=[]  else ''
        wherevar     = f" VarFlag != 0" if varflag  else '' 
        wheres = [w for w in [whereids, whereobjtype, whereoinst, wherepname, wherepval, whereptype, wheresort, wherevar] if w != '']
        return str('and'.join(wheres))




if __name__ == '__main__':
    print('test run')