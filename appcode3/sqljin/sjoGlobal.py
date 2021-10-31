from pathlib import Path
from dataclasses import dataclass

try:
    from sqljin.sjoObjectsBase import sjoObjectsBase, sjoObjectsChildren
    from sqljin.sjuUtil import sjuUtil
except:
    from sjoObjectsBase import sjoObjectsBase, sjoObjectsChildren
    from sjuUtil import sjuUtil


@dataclass
class sjoGlobal(sjoObjectsBase):
    collections: sjoObjectsChildren
    plugins: sjoObjectsChildren
    systems: sjoObjectsChildren

    def __init__(self, util: sjuUtil):
        self.util = util
        filepath = Path(str(self.util.paths.configs)) / 'Global'
        parent = None 
        super().__init__(util, filepath, parent)
        self.yamldefault = {"version":"0", "variables":{"startdate":"2021-01-01", "enddate":"2021-12-31" }}
        self.load()
        
    def _load(self) -> None:
        self.collections = self.sjoCollections(self)
        self.plugins = self.sjoPlugins(self)
        self.systems = self.sjoSystems(self)
        
    def _load_children(self) -> dict:
        rtn = self.util.paths.getFiles(self.filepath)
        for nm, val in rtn.items():
            self.log.debug(f'    {nm}')
        return rtn

    class sjoSystems(sjoObjectsChildren):
        pass 
    class sjoPlugins(sjoObjectsChildren):
        pass 
    class sjoCollections(sjoObjectsChildren):
        pass 

if __name__=='__main__':
    util = sjuUtil()
    obj = sjoGlobal(util)
