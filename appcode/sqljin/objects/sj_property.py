# ######################################################
#
# object class for all object.Properties
#
# ######################################################

from datetime import datetime
from pathlib import Path
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
    orgname: str
    objectid: int 
    eventprefix:str
    _id: int = None
    _propname: str = None 
    _propvalue: str 
    _proptype: str 
    _sort: int 
    _varflag: bool 
    _startts: str 
    data_changed: bool = None 
    autosave: bool = True
    db_passthru:bool = False

    
    def __init__(self, parentobject, loadname:str = None, newdata:dict = None, autosave:bool=True, db_passthru:bool=False) -> None:
        self.event = parentobject.event
        self.log   = parentobject.log
        self.paths = parentobject.paths
        self.objectid = parentobject.id 
        self.orgname = parentobject.orgname
        self.parentobject = parentobject
        self.eventprefix_prop = f"{self.orgname}.datamgr.prop"
        self.eventprefix_obj  = f"{self.orgname}.datamgr"
        self.db_passthru = db_passthru
        self.autosave = autosave

        if loadname is not None:
            self._id = parentobject.id
            self._propname = loadname 
            self.load()
        elif newdata is not None:
            self.assign_property_data(newdata)
        

        

        
    # Generic change functions:
    def save(self) -> bool:
        if self.data_changed or self.autosave:
            newdata = self.event.broadcast(f"{self.eventprefix_prop}.save", self)
            self.assign_property_data(newdata[0]['data'])
            return True
        else:
            self.log.debug(f"property {self.propname} in object {self.parentobject.instancename} not changed")
            return False
    
    def load(self):
        newdata = self.event.broadcast(f"{self.eventprefix_prop}.load", self)
        self.assign_property_data(newdata[0]['data'])

    def reload(self):
        self.load()

    def delete(self):
        self.event.broadcast(f"{self.eventprefix_prop}.delete", self)
        

    def assign_property_data(self, newdata:dict):
        if not self.id: self._id = newdata['id']
        if not self.propname: self._propname = newdata['propname']
        self._propvalue = newdata['propvalue']
        self._proptype = newdata['proptype']
        self._sort = newdata['sort']
        self._varflag = newdata['varflag']
        self._startts = newdata['startts']
        self.data_changed = False 
        
    
    ## ----------------------------------------------------
    ##   Property getters & setters 
    ## ----------------------------------------------------

    # ID -- Object ID, no setter
    @property
    def id(self): return self._id 

    # PROPNAME -- Property Name, no setter
    @property
    def propname(self): return self._propname


    # PROPVALUE -- Property Value
    @property
    def propvalue(self): 
        if self.db_passthru:
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.load", self)
            if rtn is not None: return rtn['data']['propvalue']
            else: return None 
        else:
            return self._propvalue

    @propvalue.setter
    def propvalue(self, newvalue):
        if self.propvalue != str(newvalue).strip(): # confirm being set to new value
            newvalue = self.apply_type(newvalue, return_native_type = False)     # confirm value works with property type
            if newvalue is None:  # if proptype error, error and escape without saving/changing
                self.log.error(f"property set failed due to data type validation failure, see messages immediately above for details")
            else:
                self._propvalue = str(newvalue)
                self.data_changed = True
                if self.autosave or self.db_passthru: self.save()


    # PROPTYPE -- Property Type
    @property
    def proptype(self): 
        if self.db_passthru:
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.load", self)
            if rtn is not None: return rtn['data']['proptype']
            else: return None 
        else:
            return self._proptype

    @proptype.setter
    def proptype(self, newvalue:str) -> bool:
        if self.proptype != str(newvalue).strip(): # confirm being set to new value
            if self.apply_type(self.propvalue, testtype = newvalue) is None:  # confirm datatype is compatible with value
                self.log.error(f"property set failed due to data type validation failure, see messages immediately above for details")
            else: # data type will work:
                self._proptype = newvalue 
                self.data_changed = True 
                if self.autosave or self.db_passthru: self.save()
                


    # SORT -- Sort Order
    @property
    def sort(self): 
        if self.db_passthru:
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.load", self)
            if rtn is not None: return rtn['data']['sort']
            else: return None 
        else:
            return self._sort
    @sort.setter
    def sort(self, newvalue:int) -> bool:
        if self.sort != newvalue: # confirm being set to new value
            self._sort = newvalue 
            self.data_changed = True 
            if self.autosave or self.db_passthru: self.save()


    # VARFLAG -- variable flag indicator
    @property
    def varflag(self): 
        if self.db_passthru:
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.load", self)
            if rtn is not None: return rtn['data']['varflag']
            else: return None
        else:
            return self._varflag

    @varflag.setter 
    def varflag(self, newvalue:bool) -> bool:
        if self.varflag != newvalue:
            self._varflag = newvalue
            self.data_changed = True 
            if self.autosave or self.db_passthru: self.save()


    # STARTTS -- Start Timestamp for the record (no setter)
    @property
    def startts(self): 
        if self.db_passthru:
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.load", self)
            if rtn is not None: return rtn['data']['startts']
            else: return None 
        else:
            return self._startts



    def apply_type(self, value:str = None, return_native_type:bool = True, testtype:str = None ):
        rtn = ''
        timeformat = ''
        proptype = testtype if testtype else self.proptype 
        if value is None: value = self.propvalue
        self.log.debug(f'applying type to propvalue (return_native_type = {return_native_type})')
        try:
            if   proptype == 'str':   rtn =  str(value).strip()
            elif proptype == 'int':   rtn =  int(value)
            elif proptype == 'dec':   rtn =  float(value)
            elif proptype == 'bool':  rtn =  bool(value)
            elif proptype == 'date': 
                rtn =  parse(value)
                timeformat = '%Y-%m-%d'
            elif proptype in ['datetime','ts', 'timestamp']: 
                rtn =  parse(value).strftime('%Y-%m-%d %H:%M:%S')
            elif proptype in ['time']: 
                rtn =  parse(value).strftime('%H:%M:%S')
            elif proptype == 'url':   
                if validators.url(value): rtn =  str(value).strip()
                else: raise Exception('type validation failed')
            elif proptype == 'email': 
                if validators.email(value): rtn =  str(value).strip()
                else: raise Exception('type validation failed')
            elif proptype == 'ip':    
                if (validators.ipv4(value) or validators.ipv6(value)): rtn =  str(value).strip() 
                else: raise Exception('type validation failed')
            elif proptype == 'path':  
                if Path(value).exists() or Path(value).parent.exists() or Path(value).parent.parent.exists():
                    rtn =  str(Path(value).resolve()).strip()
                else: raise Exception('type validation failed') 
            elif proptype == 'objlink':
                pass 
            elif proptype == 'proplink':
                pass 

            else:
                self.log.warning(f'unknown datatype during proptype validation: {proptype} in property: {self.propname}')
                return None  
            
            if return_native_type:  # return the actual python typed object
                return rtn 
            else:
                if timeformat != '': # return a string-formatted datetime
                    return rtn.strftime(timeformat)
                else:
                    return str(rtn)   # just return a string of the object
            
        except Exception as ex:
            self.log.error(f"type validation failed! {value} cannot be used as a {proptype} ({ex})")
            return None 

    def validate_type(self, newvalue) -> bool:
        adjvalue = self.apply_type(newvalue)
        return adjvalue is not None
            