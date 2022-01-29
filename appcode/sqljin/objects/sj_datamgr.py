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
        self.event.add_handler(f"{self.event_prefix}.save.id", self.save_object)
        self.event.add_handler(f"{self.event_prefix}.expire.id", self.expire_object)
        self.event.add_handler(f"{self.event_prefix}.restore.id", self.restore_object)

        # new:
        self.event.add_handler(f"{self.event_prefix}.prop.set", self.prop_set)
        self.event.add_handler(f"{self.event_prefix}.prop.get", self.prop_get)

        # old:
        self.event.add_handler(f"{self.event_prefix}.refresh.prop", self.refresh_prop)
        self.event.add_handler(f"{self.event_prefix}.save.prop", self.save_prop)
        self.event.add_handler(f"{self.event_prefix}.save.prop.dict", self.save_prop_from_dict)
        self.event.add_handler(f"{self.event_prefix}.delete.prop", self.delete_prop)
        self.event.add_handler(f"{self.event_prefix}.expire.prop", self.delete_prop)
        self.event.add_handler(f"{self.event_prefix}.restore.prop", self.restore_prop)


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
        

    # new prop methodology:
    # --------------------------------
    def prop_get(self, prop:sjprop.sj_Property):
        self.log.info(f"getting property from config.db, for object('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        rtn = self.dbConn.execute(f"""select * from Properties where ID = {prop.id} and PropName = '{prop.propname}' """, 'list')
        if rtn is None or 'data' not in rtn:
            self.log.error(f'property get failed on query, see messages immediately above for detail')
            return None 
        if len(rtn) == 0:
            self.log.error(f'property get returned zero records, this property is no longer valid and should be removed')
            self.event.broadcast(f"{self.event_prefix}.load.id", id=prop.id) # prompt object to reload
            return None 
        elif len(rtn) > 1: 
            self.log.error(f'property get returned more than one record, problem! Returning first record only!')
        return rtn[0] 

    def prop_set(self, prop:sjprop.sj_Property, newvalue, field: str = 'propvalue'):
        self.log.info(f"setting property in config.db, for object('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        if field == 'propvalue':
            val = prop.propvalue.replace("'","''")
            val = f"'{val}' as PropValue"
        else:
            val = 'PropValue'
        srt = f"{prop.sort} as Sort" if field == 'sort' else 'Sort'
        vfg = f"{prop.varflag} as Sort" if field == 'varflag' else 'VarFlag'
        typ = f"'{prop.proptype}' as PropType" if field == 'proptype' else 'PropType'
        
        rtn = self.dbConn.execute(f"""
            insert into sjProperties (ID, PropName, PropValue, Proptype, Sort, VarFlag) 
            select ID, PropName, {val}, {typ}, {srt}, {vfg} 
            from Properties 
            where ID = {prop.id} and PropName = '{prop.propname.replace("'","''")}' """)
        if rtn is None or 'rows' not in rtn: 
            self.log.error(f'property set failed on query, see messages immediately above for detail')
            return None 
        return rtn['rows']
    # --------------------------------


    def save_prop(self, prop:sjprop.sj_Property):
        self.log.debug(f"saving property ('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        self.dbConn.execute(f"""insert into sjProperties (ID, PropName, PropValue, Proptype, Sort, VarFlag) 
        values ({prop.id}, '{prop.propname}', '{prop.propvalue}', '{prop.proptype}', {prop.sort}, {prop.varflag} ) """)
        rtn = self.refresh_prop(prop)
        return rtn  

    def save_prop_from_dict(self, prop:dict):
        self.log.debug(f"saving property (dict version): {self.orgname}('{prop['id']}') {prop.propname} = {prop.propname}")
        self.dbConn.execute(f"""insert into sjProperties (ID, PropName, PropValue, Proptype, Sort, VarFlag) 
        values ({prop['id']}, '{prop['propname']}', '{prop['propvalue']}', '{prop['proptype']}', {prop['sort']}, {prop['varflag']} ) """)
        rtn = self.refresh_prop(prop)
        return rtn  

    def refresh_prop(self, prop:sjprop.sj_Property):
        self.log.info(f"refreshing property from config.db, for object('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        rtn = self.dbConn.execute(f"""select * from Properties where ID = {prop.id} and PropName = '{prop.propname}' """, 'list')
        return rtn 

    def delete_prop(self, prop:sjprop.sj_Property) -> bool:
        self.log.info(f"expiring (soft delete) property ('{prop.id}'): {prop.parentobject.orgname}.{prop.parentobject.objecttype}.{prop.parentobject.instancename}.{prop.propname}")
        prop.propvalue = '***deleted***'
        rtn = self.save_prop(prop)
        return rtn['data'] != {}

    def restore_prop(self, prop:sjprop.sj_Property):
        pass # TBD if needed




    ### function for getting many objects at once (used by Org, not Objects/Properties)
    def get_objects(self, **kwargs) -> list:
        self.log.debug(f"retrieving multiple objects (data) from '{self.orgname}' data manager")
        rtn = self.dbConn.execute(f'Select * from ObjProp where {self.get_where(kwargs)} order by ObjectType, InstanceName, ID, Sort', 'list')
        rows = rtn["data"]



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




if __name__ == '__main__':
    print('test run')