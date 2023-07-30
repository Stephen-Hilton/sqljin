# ######################################################
#
# object class for all object.Properties
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
import objects.sj_org     as sjorg



class sj_Object():

    log: sjlog.sj_Logger
    event: sjevent.sj_Event
    paths: sjpaths.sj_Paths
    utils: dict 

    org: object # sjorg.sj_Org
    orgname: str 

    id: int 
    objecttype: str
    instancename: str 
    active: bool
    props: dict 

    data_changed:bool = False
    handlers_added:bool = False 
    _status:str = 'empty'
    eventprefix:str = None

    def __init__(self, utils:dict, parentOrg:object) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.utils = utils 
        self.org = parentOrg
        self.orgname = parentOrg.name 



    def add_handlers(self):
        if not self.handlers_added:
            self.eventprefix = f"{ self.orgname}.{self.objecttype}.{self.instancename}" 
            self.event.add_handler(f"{self.eventprefix}.load", self.load)
            self.event.add_handler(f"{self.eventprefix}.save", self.save)
            self.event.add_handler(f"{self.eventprefix}.expire", self.expire)
            self.event.add_handler(f"{self.eventprefix}.restore", self.restore)
            self.event.add_handler(f"{self.eventprefix}.remove.deleted", self.allprops_remove_deleted)
            self.event.add_handler(f"{self.eventprefix}.sort", self.allprops_sort)
            self.event.add_handler(f"{self.eventprefix}.status", self.set_status)
            self.event.add_handler(f"{self.eventprefix}.add.prop", self.prop_add)

            self.event.add_handler(f"user.request.refresh.all", self.load)
            self.event.add_handler(f"user.request.refresh.{ self.objecttype }", self.load)
            self.event.add_handler(f"user.request.refresh.{ self.objecttype }s", self.load)
            self.event.add_handler(f"user.request.refresh.{ self.orgname }", self.load)

            self.handlers_added = True

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, newstatus:str):
        self._status = newstatus
        if self.eventprefix:
            self.event.broadcast(f"{self.eventprefix}.status.changed", self)
    def set_status(self, newstatus:str): # for the event
        self.status = newstatus


    def build_properties(self, propdata) -> dict:
        self.log.debug('rebuilding all properties from data')
        self.props = {}
        for row in propdata:
            if row['propvalue'] != '***deleted***':
                self.prop_add(row['propname'], row['propvalue'], row['proptype'], row['sort'], row['varflag'], row['startts'])
        return self.props


    def load(self):
        objdata = self.event.narrowcast(f"{self.orgname}.datamgr.load.id", self.id)

        if (not objdata) or ("data" not in objdata) or (len(objdata["data"])==0):
            self.log.error(f"event ({self.orgname}.datamgr.load.id) returned no data, aborting load")
            return False 

        data = objdata["data"]
        self.id           = int(data[0]['id'])
        self.objecttype   = str(data[0]['objecttype'])
        self.instancename = str(data[0]['instancename'])
        self.active       = bool(data[0]['active'])
        self.props = self.build_properties(data)
        self.status = 'loaded'
        self.data_changed = False 

        self.log.info(f"object {self.eventprefix} loaded")
        self.event.broadcast(f"{self.eventprefix}.loaded", id=self.id, type=self.objecttype, name=self.instancename, org=self.org)
        return True

        


    def save(self):
        return self.event.broadcast(f"{self.orgname}.datamgr.save", self)

    def expire(self):
        return self.event.broadcast(f"{self.orgname}.datamgr.expire", self)

    def restore(self):
        return self.event.broadcast(f"{self.orgname}.datamgr.restore", self)


    # Property functions
    def getprop(self, propname:str, default = None) -> str:
        if propname in self.props:  
            return self.props[propname].apply_type()
        elif default is not None:
            return default 
        else: 
            return None 

    def setprop(self, propname, value) -> str:
        if propname in self.props:
            self.props[propname].propvalue = value 
            return self.getprop(propname)


    def prop_add(self, propname:str, propvalue:str='', proptype:str='str', sort:int=500, varflag:bool = True, startts:str=''):
        prop = sjprop.sj_Property(self, propname, propvalue, proptype, sort, varflag, startts )
        self.props[prop.propname] = prop 
        self.log.debug(f'property added: {self.orgname}.{self.objecttype}.{self.instancename}.{prop.propname} ({prop.proptype}) = {prop.propvalue}')
        return prop 

    def allprops_sort(self):
        self.log.debug(f"sorting properties within object")
        pass

    def allprops_save(self):
        for prop in self.props:
            prop.save()

    def allprops_reload(self):
        for prop in self.props:
            prop.reload()

    def allprops_remove_deleted(self) -> dict:
        newprops = {}
        for prop in self.props:
            if prop.propvalue != '***deleted***' or prop.data_changed is not None:
                newprops[prop.propname] = prop 
        self.props = newprops
        self.event.broadcast(f"{self.eventprefix}.props.loaded", self)

