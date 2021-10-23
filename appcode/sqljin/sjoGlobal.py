from pathlib import Path
from dataclasses import dataclass

try:
    from sqljin.sjoObjectBase import sjoObjectBase
    from sqljin.sjuUtil import sjuUtil
except:
    from sjoObjectBase import sjoObjectBase
    from sjuUtil import sjuUtil


@dataclass
class sjoGlobal(sjoObjectBase):
    collections: dict 
    plugins: dict
    systems: dict     

    def __init__(self, util: sjuUtil):
        self.util = util
        filepath = Path(str(self.util.paths.configs)) / 'Global'
        parent = None 
        super().__init__(util, filepath, parent)
        self.variables.default = {"version":"0", "variables":{"startdate":"2021-01-01", "enddate":"2021-12-31" }}
        self.variables.downloadable = True
        self.load()
        
        
    def _load_children(self) -> dict:
        rtn = self.util.paths.getFiles(self.filepath)
        for nm, val in rtn.items():
            self.log.debug(f'    {nm}')
        return rtn


if __name__=='__main__':
    util = sjuUtil()
    obj = sjoGlobal(util)
