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
    _id: int
    _propname: str 
    
    def __init__(self, parentobject, loadname:str = None, newdata:dict = None) -> None:
        self.event = parentobject.event
        self.log   = parentobject.log
        self.paths = parentobject.paths
        self.objectid = parentobject.id 
        self.parentorg = parentobject.orgname
        self.eventprefix_prop = f"{self.orgname}.datamgr.prop"
        self.eventprefix_obj  = f"{self.orgname}.datamgr"

        if loadname is not None:
            self._id = parentobject.id
            self._propname = loadname 
        elif newdata is not None:
            try:
                self._id = newdata['id']
                self._propname = newdata['propname']
            except KeyError as ex:
                self.log.error(f'issue loading new property - malformed newdata dictionary (program error): {newdata}')
        # everything else is a real-time lookup from config.db


        
    
    ## ----------------------------------------------------
    ##   Property getters & setters -- now just pass-thru 
    ##   functions that get/set to config.db directly
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
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.get", prop=self)
        if rtn is not None: return rtn['data']['propvalue']
        else: return None 
    @propvalue.setter
    def propvalue(self, newvalue):
        newvalue = self.apply_type(newvalue)
        if newvalue is not None:
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.set", prop=self, newvalue=newvalue, field='propvalue' ) 
            if rtn is None: self.log.error(f'property set failed: {self.propname} ')
        else:
            self.log.error(f"property set failed due to data type validation failure, see messages immediately above for details")


    # PROPTYPE -- Property Type
    @property
    def proptype(self): 
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.get", prop=self)
        if rtn is not None: return rtn['data']['proptype']
        else: return None 
    @proptype.setter
    def proptype(self, newvalue:str) -> bool:
        currentpropvalue = self.propvalue 
        if self.validate_type(currentpropvalue): # validate existing value will work with new type
            rtn = self.event.broadcast(f"{self.eventprefix_prop}.set", prop=self, newvalue=newvalue, field='proptype' ) 
            if rtn is None: self.log.error(f'property set failed: {self.propname} ')
        else:
            self.log.error(f"property set failed due to data type validation failure, see messages immediately above for details")


    # SORT -- Sort Order
    @property
    def sort(self): 
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.get", prop=self)
        if rtn is not None: return rtn['data']['sort']
        else: return None 
    @sort.setter
    def sort(self, newvalue:int) -> bool:
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.set", prop=self, newvalue=newvalue, field='sort' ) 
        if rtn is None: self.log.error(f'property set failed: {self.propname} ')


    # VARFLAG -- variable flag indicator
    @property
    def varflag(self): 
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.get", prop=self)
        if rtn is not None: return rtn['data']['varflag']
        else: return None 
    @varflag.setter 
    def varflag(self, newvalue:bool) -> bool:
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.set", prop=self, newvalue=newvalue, field='varflag' ) 
        if rtn is None: self.log.error(f'property set failed: {self.propname} ')


    # STARTTS -- Start Timestamp for the record (no setter)
    @property
    def startts(self): 
        rtn = self.event.broadcast(f"{self.eventprefix_prop}.get", prop=self)
        if rtn is not None: return rtn['data']['startts']
        else: return None 



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
            