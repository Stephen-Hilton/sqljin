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
import objects.sj_orgs     as sjorg



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
    _status_:str = 'empty'
    eventprefix:str = None

    def __init__(self, utils:dict, parentOrg:object, loadcriteria = None) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.utils = utils 
        self.org = parentOrg
        self.orgname = parentOrg.name 

        if loadcriteria is not None:
            if   type(loadcriteria) is dict:
                objdata = loadcriteria.data 
            elif type(loadcriteria) is int:
                objdata = self.event.broadcast(f"{self.orgname}.datamgr.load.id", loadcriteria )
            elif type(loadcriteria) is tuple:
                objdata = self.event.broadcast(f"{self.orgname}.datamgr.load.typename", loadcriteria[0], loadcriteria[1] )
            else: 
                self.log.error(f'New object requested in {self.orgname}, but unknown loadcritiera provided (probably programming mistake) - returning a blank object')   
                return None ##
        else:
            self.log.warning(f'New object requested: {self.orgname}, but no data provided or found (or is an Organization) - returning a blank object.')
            return None ##
        
        self.assign_object_data(objdata)
        self.add_handlers()
    


    def assign_object_data(self, objdata) -> bool:
        if 'data' not in objdata:
            self.log.error(f'object data invalid: {str(objdata)}')
            return False ##

        data = objdata["data"]
        if len(data) == 0: 
            self.log.error(f'object returned no data from config.db, make sure object still exists / is active')
            return False ##

        self.id           = int(data[0]['id'])
        self.objecttype   = str(data[0]['objecttype'])
        self.instancename = str(data[0]['instancename'])
        self.active       = bool(data[0]['active'])
        self.props = self.build_properties(data)
        self.status = 'loaded'
        return True


    def add_handlers(self):
        if not self.handlers_added and self.status == 'loaded':
            self.eventprefix = f"{ self.orgname}.{self.objecttype}.{self.instancename}" 
            self.event.add_handler(f"{self.eventprefix}.load", self.load)
            self.event.add_handler(f"{self.eventprefix}.save", self.save)
            self.event.add_handler(f"{self.eventprefix}.expire", self.expire)
            self.event.add_handler(f"{self.eventprefix}.restore", self.restore)
            self.event.add_handler(f"{self.eventprefix}.remove.deleted", self.allprop_remove_deleted)
            self.event.add_handler(f"{self.eventprefix}.sort", self.allprop_sort)
            self.event.add_handler(f"{self.eventprefix}.status", self.set_status)
            self.event.add_handler(f"{self.eventprefix}.add.prop", self.prop_add)
            self.handlers_added = True

    @property
    def status(self):
        return self._status_

    @status.setter
    def status(self, newstatus:str):
        self._status_ = newstatus
        if self.eventprefix:
            self.event.broadcast(f"{self.eventprefix}.status.changed", self)
    def set_status(self, newstatus:str): # for the event
        self.status = newstatus


    def build_properties(self, propdata) -> dict:
        self.log.debug('rebuilding all properties from data')
        self.props = {}
        for row in propdata:
            if row['propvalue'] != '***deleted***':
                prop = self.prop_add(row['propname'], row['propvalue'], row['proptype'], row['sort'], row['varflag'], row['startts'])
                self.props[prop.propname] = prop 
        return self.props


    def load(self):
        objdata = self.event.broadcast(f"{self.orgname}.datamgr.load.id", self.id)
        if len(objdata) >1:
            self.log.error(f"event ({self.orgname}.datamgr.load.id) returned more than one result, using first one found")
            self.log.error(f"this can happen if event has more than one handler")
        objdata = objdata[0] # always do this

        if len(objdata) == 0 or "data" not in objdata:
            self.log.error(f"event ({self.orgname}.datamgr.load.id) returned no data, aborting load")
            return False 
        
        self.assign_object_data(objdata)
        if not self.handlers_added: self.add_handlers()
        self.log.info(f"object {self.orgname}.{self.objecttype}.{self.instancename} loaded")


    def save(self):
        return self.event.broadcast(f"{self.orgname}.datamgr.save.id", self)

    def expire(self):
        return self.event.broadcast(f"{self.orgname}.datamgr.expire.id", self)

    def restore(self):
        return self.event.broadcast(f"{self.orgname}.datamgr.restore.id", self)


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


    def prop_add(self, propname:str, propvalue:str='', proptype:str='str', sort:int=500, varflag:bool = True, startts:str = ''):
        prop = sjprop.sj_Property(self, propname, propvalue, proptype, sort, varflag, startts)
        self.props[prop.propname] = prop 
        self.log.debug(f'property added: {self.orgname}.{self.objecttype}.{self.instancename}.{propname} ({proptype}) = {propvalue}')
        return prop 

    def allprop_sort(self):
        self.log.debug(f"sorting properties within object")
        pass

    def allprop_save(self):
        for prop in self.props:
            prop.save()

    def allprop_reload(self):
        for prop in self.props:
            prop.reload()

    def allprop_remove_deleted(self) -> dict:
        newprops = {}
        for prop in self.props:
            if prop.propvalue != '***deleted***':
                newprops[prop.propname] = prop 
        self.props = newprops

