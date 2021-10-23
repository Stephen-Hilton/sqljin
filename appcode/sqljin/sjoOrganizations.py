from pathlib import Path
from dataclasses import dataclass

try:
    from sqljin.sjoObjectsBase import sjoObjectsBase
    from sqljin.sjuUtil import sjuUtil
except:
    from sjoObjectsBase import sjoObjectsBase
    from sjuUtil import sjuUtil


@dataclass
class sjoOrganizations(sjoObjectsBase):
    collections: dict 
    plugins: dict
    systems: dict     

    def __init__(self, util: sjuUtil, filepath:Path, parent:object):
        super().__init__(util, filepath, parent)
        self.variables.default = {"version":"0", "variables":{  "organization.name":"OrgName Here", 
                                                                "organization.website": "http://example.com",
                                                                "organization.contact":"person@company.com",   
                                                                "remember_credentials":True }}
        self.variables.downloadable = True
        self.load()


    def load(self) -> None:
        self.load_systems()
        self.load_collections()
        self.load_plugins()


    def load_systems(self) -> dict:
        syspath = self._load_stuff('systems')
        


    def load_collections(self) -> dict:
        self._load_stuff('collections')

    def load_plugins(self) -> dict:
        self._load_stuff('plugins')
        for subdir in ['dbconnections','execution_tasks','historic_run_actions']:
            Path.mkdir( self.filepath / 'plugins' / subdir, parents=True, exist_ok=True)
        

    def _load_stuff(self, thing_to_load:str) -> Path:
        filepath = self.filepath / thing_to_load
        self.log.debug(f'loading objects "{thing_to_load}" from: {filepath}')
        return Path.mkdir(filepath, parents=True, exist_ok=True)





if __name__=='__main__':
    util = sjuUtil()
    obj = sjoOrganizations(util, Path('C:\git\sqljin\configs\organizations\Teradata'), None)

