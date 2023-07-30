from pathlib import Path
import importlib
import sys

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_object   as sjobject

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths

class sj_System(sjobject.sj_Object):

    @property
    def host(self): self.getprop('host', '-- not set --')
    @host.setter
    def host(self, value): return self.setprop('host', value) 

    @property
    def driver(self): self.getprop('driver', '-- not set --')
    @host.setter
    def driver(self, value): return self.setprop('driver', value) 

    @property
    def encrypt(self): self.getprop('encrypt', '-- not set --')
    @host.setter
    def encrypt(self, value): return self.setprop('encrypt', value) 

    @property
    def logmech(self): self.getprop('logmech', '-- not set --')
    @host.setter
    def logmech(self, value): return self.setprop('logmech', value) 

    @property
    def credentials(self): self.getprop('credentials', '-- not set --')
    @host.setter
    def credentials(self, value): return self.setprop('credentials', value) 
    

    