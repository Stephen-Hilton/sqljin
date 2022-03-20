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
import objects.sj_org     as sjorg


class sj_Property():
    log:   sjlog.sj_Logger
    event: sjevent.sj_Event
    paths: sjpaths.sj_Paths
    orgname: str
    eventprefix:str
    _id: int = None
    _propname: str = None 
    _proptype: str = None 
    _propvalue: str = None 
    _sort: int = None 
    _varflag: bool = None 
    _startts: str = None 
    data_changed: bool = False 
    type_error: bool = False

    # ordered most restrictive to least (tested in this order)
    valid_types =  ['url','email','ip','timestamp','ts','time','date','datetime','path','bool','objlink','proplink','dec','int','str'] 
    
    def __init__(self, parentobject, propname:str, propvalue:str='', proptype:str='str', sort:int=500, varflag:bool = True, startts:str='') -> None:
        self.event = parentobject.event
        self.log   = parentobject.log
        self.paths = parentobject.paths
        self.orgname = parentobject.orgname
        self.parentobject = parentobject
        self.eventprefix_prop = f"{self.orgname}.datamgr.prop"
        self.eventprefix_obj  = f"{self.orgname}.datamgr"
        
        self._id = parentobject.id
        self._propname = propname
        self._proptype = proptype if proptype in self.valid_types else 'str'
        self.propvalue = propvalue
        self.sort = sort
        self.varflag = varflag
        self._startts = startts 
        self.data_changed = False 

        

    def delete(self):
        self.event.broadcast(f"{self.eventprefix_prop}.delete", self)

        
        
    
    ## ----------------------------------------------------
    ##   Property GETTERS
    ## ----------------------------------------------------
    
    @property
    def id(self): return self._id 

    @property
    def propname(self): return self._propname

    @property
    def propvalue(self):  return self._propvalue

    @property
    def proptype(self):  return self._proptype

    @property
    def sort(self):  return self._sort

    @property
    def varflag(self):  return self._varflag

    @property
    def startts(self): return self._startts


    ## ----------------------------------------------------
    ##   Property SETTERS
    ## ----------------------------------------------------

    # ID -- Object ID, no setter
    # PROPNAME -- Property Name, no setter
    # STARTTS -- Start Timestamp for the record, no setter

    # PROPVALUE
    @propvalue.setter
    def propvalue(self, newvalue):
        if self.propvalue != str(newvalue).strip(): # confirm being set to new value
            newvalue = self.apply_type(newvalue, return_native_type = False)     # confirm value works with property type
            if newvalue is None:  # if proptype error, error and escape without saving/changing
                self.log.error(f"property set failed due to data type validation failure, see messages immediately above for details")
            else:
                self._propvalue = str(newvalue)
                self.data_changed = True

    # PROPTYPE
    @proptype.setter
    def proptype(self, newvalue:str) -> bool:
        if self.proptype != str(newvalue).strip(): # confirm being set to new value
            if self.apply_type(self.propvalue, testtype = newvalue) is None:  # confirm datatype is compatible with value
                self.log.error(f"property set failed due to data type validation failure, see messages immediately above for details")
            else: # data type will work:
                self._proptype = newvalue 
                self.data_changed = True 
                
    # SORT
    @sort.setter
    def sort(self, newvalue:int) -> bool:
        if self.sort != newvalue: # confirm being set to new value
            self._sort = newvalue 
            self.data_changed = True 

    # VARFLAG
    @varflag.setter 
    def varflag(self, newvalue:bool) -> bool:
        if self.varflag != newvalue:
            self._varflag = newvalue
            self.data_changed = True 

    




    def apply_type(self, value:str = None, return_native_type:bool = True, testtype:str = None, log:bool = True) -> str:
        rtn = ''
        timeformat = ''
        proptype = testtype if testtype else self.proptype 
        if value is None: value = self.propvalue
        if log: self.log.debug(f'applying type to propvalue (return_native_type = {return_native_type})')
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
                if log: self.log.warning(f'unknown datatype during proptype validation: {proptype} in property: {self.propname}')
                self.type_error = True
                return None  
            
            self.type_error = False
            if return_native_type:  # return the actual python typed object
                return rtn 
            else:
                if timeformat != '': # return a string-formatted datetime
                    return rtn.strftime(timeformat)
                else:
                    return str(rtn)   # just return a string of the object
            
        except Exception as ex:
            if log: self.log.error(f"type validation failed! {value} cannot be used as a {proptype} ({ex})")
            self.type_error = True
            return None 

    def autodetect_type(self, newvalue:str) ->str:
        for objtype in self.valid_types:
            if self.apply_type(newvalue):
                return objtype