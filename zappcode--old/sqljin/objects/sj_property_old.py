# ######################################################
#
# object class for all object.Properties
#
# ######################################################

from datetime import datetime
from pathlib import Path
import os 
from dateutil.parser import parse
import validators

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
    parentobject: object # sjobject.sj_Object
    parentorg: object # sjorg.sj_Org
    eventprefix:str
    _data_changed:list 
    
    def __init__(self, parentobject, propname:str, propvalue:str='str', proptype:str='str', sort:int=500, varflag:bool=True, startts:str='') -> None:
        self.event = parentobject.event
        self.log   = parentobject.log
        self.paths = parentobject.paths
        self.parentobject = parentobject
        self.parentorg = parentobject.org
        self.eventprefix = f"{self.parentorg.name}.{self.parentobject.objecttype}.{self.parentobject.instancename}.prop"

        self._id = parentobject.id
        self._propname = propname
        self._propvalue = propvalue 
        self._proptype = proptype
        self._sort = sort 
        self._varflag = varflag
        self._startts = startts if startts !='' else str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
        self._data_changed = []
        
    # Generic change functions:
    def save(self) -> bool:
        if self.data_changed != []:
            newdata = self.utils['event'].broadcast(f"{self.parentobject.orgname}.datamgr.save.prop", self)
            self.assign_property_data(newdata[0]['data'])
            return True
        else:
            self.utils['log'].debug(f"property {self.propname} in object {self.parentobject.instancename} not changed")
            return False
    
    def reload(self):
        newdata = self.utils['event'].broadcast(f"{self.parentobject.orgname}.datamgr.refresh.prop", self)
        self.assign_property_data(newdata[0]['data'])


    def delete(self):
        self.log.debug(f"expiring (soft-delete) property {self.propname}")
        self._propvalue = '***deleted***'
        self.parentobject.allprop_remove_deleted()




    def assign_property_data(self, newdata:dict):
        if not self.id: self.id = newdata['id']
        if not self.propname: self.propname = newdata['propname']
        self.propvalue = newdata['propvalue']
        self.proptype = newdata['proptype']
        self.sort = newdata['sort']
        self.varflag = newdata['varflag']
        self.startts = newdata['startts']
        self.data_changed = []
            



    
    ## ----------------------------------------------------
    ##   Property getters & setters
    ## ----------------------------------------------------

    
    # ID -- Object ID
    @property
    def id(self): return self._id 
    @id.setter
    def id(self, value):
        self.log.error(f'{self.propname} - properties cannot move between objects, try making a copy instead')
        return False

    # PROPNAME -- Property Name
    @property
    def propname(self): return self._propname
    @propname.setter
    def propname(self, value:str) -> bool:
        self.log.error(f'{self.propname} - property name cannot be changed, try making a copy instead')
        return False

    # PROPVALUE -- Property Value
    @property
    def propvalue(self): return self._propvalue
    @propvalue.setter
    def propvalue(self, newvalue):
        if self._propvalue != newvalue:
            newvalue = self.apply_type(newvalue)
            if newvalue is not None:
                oldvalue = self._propvalue
                self._propvalue = newvalue
                self.data_changed = 'propvalue'
                self.event.broadcast(f"{self.eventprefix}.{self.propname}.value.changed", prop=self, oldvalue=oldvalue, newvalue=newvalue)
            else:
                self.log.error(f"failed to change property {self.propname}")

    # PROPTYPE -- Property Type
    @property
    def proptype(self): return self._proptype
    @proptype.setter
    def proptype(self, newtype:str) -> bool:
        if self._proptype != newtype:
            oldtype = self._proptype
            self._proptype = newtype
            if self.validate_type(self._propvalue):
                self.data_changed = 'proptype'
                self.event.broadcast(f"{self.eventprefix}.{self.propname}.type.changed", prop=self, oldtype=oldtype, newtype=self._proptype)
            else:
                self._proptype = oldtype # revert 
                self.log.error(f"failed to change property {self.propname}")

    # SORT -- Sort Order
    @property
    def sort(self): return self._sort
    @sort.setter
    def sort(self, newsort:int) -> bool:
        if self._sort != newsort:
            oldsort = self._sort
            self._sort = newsort
            self.data_changed = 'sort'
            self.event.broadcast(f"{self.eventprefix}.{self.propname}.sort.changed", prop=self, oldsort=oldsort, newsort=newsort)

    # VARFLAG -- Is-A-Variable Flag
    @property
    def varflag(self): return self._varflag
    @varflag.setter 
    def varflag(self, newflag:bool) -> bool:
        if self._varflag != newflag:
            self._varflag = 1 if newflag else 0
            self.data_changed = 'varflag'
            self.event.broadcast(f"{self.eventprefix}.{self.propname}.varflag.changed", prop=self, oldflag=not newflag, newflag=newflag)

    # STARTTS -- Start Timestamp for the record (no setter)
    @property
    def startts(self): return self._startts
    @startts.setter
    def startts(self, value:str) -> bool:
        self.log.error(f'{self.propname} - property start timestamp is automatically managed, and cannot be manually set')
        return False

    @property
    def data_changed(self):  return self._data_changed
    @data_changed.setter
    def data_changed(self, fld:str='propvalue'):
        if fld not in self._data_changed: 
            self._data_changed.append(fld)
            self.event.broadcast(f"{self.eventprefix}.changed", prop=self, changed=fld)


    def validate_change(self, changefield:str = 'propvalue', oldvalue = None, newvalue = None) -> bool:
        if changefield in ['propvalue','proptype','sort','varflag','startts']:    
            if self.validate_datatype(newvalue):    
                self._data_changed
                self.event.broadcast(f"{self.eventprefix}.changed", prop=self, changefield=changefield, oldvalue=oldvalue, newvalue=newvalue)
                self.event.broadcast(f"{self.eventprefix}.{self.propname}.{changefield}.changed", prop=self, oldvalue=oldvalue, newvalue=newvalue)
        elif changefield in ['id','propname']:
            self.log.error(f'property {changefield} cannot be modified, try cloning a property instead')
        else: 
            self.log.error(f'unknown field: {changefield} - definitely a program error')



    def apply_type(self, value:str = None, return_native_type:bool = True):
        rtn = ''
        timeformat = ''
        if value is None: value = self.propvalue
        self.log.debug(f'applying type to propvalue (return_native_type = {return_native_type})')
        try:
            if   self.proptype == 'str':   rtn =  str(value)
            elif self.proptype == 'int':   rtn =  int(value)
            elif self.proptype == 'dec':   rtn =  float(value)
            elif self.proptype == 'bool':  rtn =  bool(value)
            elif self.proptype == 'date': 
                rtn =  parse(value)
                timeformat = '%Y-%m-%d'
            elif self.proptype in ['datetime','ts', 'timestamp']: 
                rtn =  parse(value).strftime('%Y-%m-%d %H:%M:%S')
            elif self.proptype in ['time']: 
                rtn =  parse(value).strftime('%H:%M:%S')
            elif self.proptype == 'url':   
                if validators.url(value): rtn =  str(value).strip()
                else: raise Exception('type validation failed')
            elif self.proptype == 'email': 
                if validators.email(value): rtn =  str(value).strip()
                else: raise Exception('type validation failed')
            elif self.proptype == 'ip':    
                if (validators.ipv4(value) or validators.ipv6(value)): rtn =  str(value).strip() 
                else: raise Exception('type validation failed')
            elif self.proptype == 'path':  
                if Path(value).exists() or Path(value).parent.exists() or Path(value).parent.parent.exists():
                    rtn =  str(Path(value).resolve()).strip()
                else: raise Exception('type validation failed') 
            elif self.proptype == 'objlink':
                pass 
            elif self.proptype == 'proplink':
                pass 

            else:
                self.log.warning(f'unknown datatype during proptype validation: {self.proptype} in property: {self.propname}')
                return None  
            
            if return_native_type:  # return the actual python typed object
                return rtn 
            else:
                if timeformat != '': # return a string-formatted datetime
                    return rtn.strftime(timeformat)
                else:
                    return str(rtn)   # just return a string of the object
            
        except Exception as ex:
            self.log.error(f"type validation failed! {value} cannot be used as a {self.proptype} ({ex})")
            return None 

    def validate_type(self, newvalue) -> bool:
        adjvalue = self.apply_type(newvalue)
        return adjvalue is not None
            