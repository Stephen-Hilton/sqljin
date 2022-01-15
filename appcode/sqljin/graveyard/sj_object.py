from pathlib import Path
# from .sj_orgs import sj_Org
# from .sj_event import sj_Event
# from .sj_logger import sj_Logger
# from .sj_paths import sj_Paths



class sjprop():
    def __init__(self, org:object, id:int, propname:str, propvalue:str, proptype:str, sort:int, varflag:bool, startts:str) -> None:
        self.org = org
        self._id = id 
        self._propname = propname
        self._propvalue = propvalue 
        self._proptype = proptype
        self._sort = sort 
        self._varflag = varflag
        self._startts = startts
        
    # Generic change functions:
    def update(self) -> bool:
        rtn = 'success'
        if rtn=='success': success = self.reload()


    # ID -- Object ID
    @property
    def id(self): return self._id 
    
    @property.setter
    def id(self, value:int) -> bool:
        org.log.error(f'properties cannot move between objects: {self.propname}')
        return False

    # PROPNAME -- Property Name
    @property
    def propname(self): return self._propname


    @property
    def propvalue(self): return self._propvalue
    @property
    def proptype(self): return self._proptype
    @property
    def sort(self): return self._sort
    @property
    def varflag(self): return self._varflag
    @property
    def startts(self): return self._startts





if __name__ == "__main__":
    o = sjprop(None, 1,'label', 'poop', 'str', 50, False, '')
    print( o.propname )

    o.id = 12
    print(o.id)