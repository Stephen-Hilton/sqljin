# ######################################################
#
# object class for all object.Properties
#
# ######################################################

from pathlib import Path

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths


import objects.sj_datamgr  as sjdatamgr  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject  
import objects.sj_orgs     as sjorg


class sj_Property():
    log:   sjlog.sj_Logger
    event: sjevent.sj_Event
    paths: sjpaths.sj_Paths
    parentObject: sjobject.sj_Object
    parentOrg: object #sjorg.sj_Org
    
    def __init__(self, parentObject:sjobject.sj_Object, propname:str, propvalue:str, proptype:str, sort:int, varflag:bool, startts:str) -> None:
        self.event = parentObject.event
        self.log   = parentObject.log
        self.paths = parentObject.paths
        self.parentObject = parentObject
        self.parentOrg = parentObject.parentOrg

        self._id = parentObject.id
        self._propname = propname
        self._propvalue = propvalue 
        self._proptype = proptype
        self._sort = sort 
        self._varflag = varflag
        self._startts = startts
        self.data_changed = False
        
    # Generic change functions:
    def save(self) -> bool:
        if self.data_changed == True:
            # save current changes using the datamanager
            self.event.broadcast(f'{self.parent_object.orgname}.{self.parent_object.objecttype}.{self.parent_object.instancename}.{self.propname}.SAVED')
            self.data_changed = False
        
    def reload(self) -> bool:
        # prompt parent object to reload from db
        pass 

    def rollback(self) -> bool:
        return self.reload()

    
    ## ----------------------------------------------------
    ##   Property getters & setters
    ## ----------------------------------------------------

    # PARENT OBJECT  (no setter - just for reference)
    @property
    def parent_object(self): return self._parent_object
    
    # ID -- Object ID
    @property
    def id(self): return self._id 
    @id.setter
    def id(self, value):
        self.log.error(f'properties cannot move between objects: {self.propname}')
        return False

    # PROPNAME -- Property Name
    @property
    def propname(self): return self._propname
    @propname.setter
    def propname(self, value:str) -> bool:
        self.log.error(f'property name cannot be changed, try to copy the propery instead: {self.propname}')
        return False

    # PROPVALUE -- Property Value
    @property
    def propvalue(self): return self._propvalue
    @propvalue.setter
    def propvalue(self, newvalue, newtype:str=None):
        if self._propvalue != newvalue:
            if self.validate_datatype(newvalue, newtype):
                self._propvalue = newvalue
                self.data_changed = True
                self.event.broadcast(f'{self.parent_object.orgname}.{self.parent_object.objecttype}.{self.parent_object.instancename}.{self.propname}.CHANGED', prop=self, changed='propvalue', old=self._propvalue, new=newvalue)
            else:
                self.log.error(f"data type '{newtype}' not valid for property value {newvalue}, change not saved.")

    # PROPTYPE -- Property Type
    @property
    def proptype(self): return self._proptype
    @proptype.setter
    def proptype(self, newtype:str) -> bool:
        if self._proptype != newtype:
            if self.validate_datatype(self.propvalue, newtype):
                self._proptype = newtype
                self.data_changed = True
                self.event.broadcast(f'{self.parent_object.orgname}.{self.parent_object.objecttype}.{self.parent_object.instancename}.{self.propname}.CHANGED', prop=self, changed='proptype', old=self._proptype, new=newtype)
            else:
                self.log.error(f"data type '{newtype}' not valid for property value {self.propvalue}, change not saved.")

    # SORT -- Sort Order
    @property
    def sort(self): return self._sort
    @sort.setter
    def sort(self, newsort:int) -> bool:
        if self._sort != newsort:
            self._sort = newsort
            self.data_changed = True
            self.event.broadcast(f'{self.parent_object.orgname}.{self.parent_object.objecttype}.{self.parent_object.instancename}.{self.propname}.CHANGED_SORT', prop=self, changed='sort', old=self._sort, new=newsort)

    # VARFLAG -- Is-A-Variable Flag
    @property
    def varflag(self): return self._varflag
    @varflag.setter 
    def varflag(self, newflag:bool) -> bool:
        if self._varflag != newflag:
            self._varflag = 1 if newflag else 0
            self.data_changed = True
            self.event.broadcast(f'{self.parent_object.orgname}.{self.parent_object.objecttype}.{self.parent_object.instancename}.{self.propname}.CHANGED', prop=self, changed='varflag', old=self._varflag, new=newflag )

    # STARTTS -- Start Timestamp for the record (no setter)
    @property
    def startts(self): return self._startts

    def validate_datatype(self, propvalue, proptype=None) -> bool:
        # validate that the value will work given the datatype
        return True
        

class sj_Properties():
    log:   sjlog.sj_Logger
    event: sjevent.sj_Event
    paths: sjpaths.sj_Paths
    parentObject: sjobject.sj_Object
    parentOrg: object # sjorg.sj_Org

    _properties = []
    _resort = False

    def __init__(self, parentObject:sjobject.sj_Object, properties:list = None) -> None:
        self.event = parentObject.event
        self.log   = parentObject.log
        self.paths = parentObject.paths
        self.parentObject = parentObject
        self.parentOrg = parentObject.parentOrg
        if properties is not None: 
            self.properties = properties

    @property
    def properties(self) -> list:
        if self._resort:
            pass # re-sort list
        return self._properties

    @property
    def properties_with_history(self) -> list:
        if self._resort:
            pass # re-sort list
        return self._properties

    @property
    def properties_with_deleted(self) -> list:
        if self._resort:
            pass # re-sort list
        return self._properties

    def load_properties(self, properties:list = None) ->None:
        # properties is a list of dictionaries
        if properties is None: properties = self.properties
        