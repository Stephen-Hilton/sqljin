from pathlib import Path
from dataclasses import dataclass
import yaml

try:
    from sqljin.sjoObjectBase import sjoObjectBase
    from sqljin.sjuUtil import sjuUtil
except:
    from sjoObjectBase import sjoObjectBase
    from sjuUtil import sjuUtil


@dataclass
class sjoSystem(sjoObjectBase):
    credentials: tuple
    host:str
    store_password:bool
    login_mechanism: str 
    encrypt: bool
    plugin_filepath: Path
    plugin: object

    def __init__(self, util: sjuUtil, filepath:Path, parent:object):
        super().__init__(util, filepath, parent)
        self.variables.default = {"version":"0", "host":"dns.or.ip.address", "logmech":"", 
                                  "encrypt":False, "plugin":"test.py", "username":"your_name",
                                  "password":"TBD", "variables":{"process name":{"name":"value","name2":"value2"} }}
        self.variables.downloadable = False
        self.variables.filepath = self.filepath # let the variable process open the system file
        self.load()
        
    def load(self) -> dict:
        super().load()
        

        

if __name__=='__main__':
    util = sjuUtil()
    obj = sjoSystem(util, Path('C:\git\sqljin\configs\organizations\Teradata\systems\Transcend.yaml'), None)
    obj.load()
