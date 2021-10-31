from pathlib import Path
from dataclasses import dataclass
import json

try:
    from sqljin.sjuLog import sjuLog
    from sqljin.sjuEvent import sjuEvent
    from sqljin.sjuPath import sjuPath
    from sqljin.sjuUtil import sjuUtil
    from sqljin.sjoObjectBase import sjoObjectBase
except:
    from sjuLog import sjuLog
    from sjuEvent import sjuEvent
    from sjuPath import sjuPath
    from sjuUtil import sjuUtil
    from sjoObjectBase import sjoObjectBase


@dataclass
class sjoObjectsBase(sjoObjectBase):

    def __init__(self, util: sjuUtil, filepath: Path, parent: object = None):
        super().__init__(util, filepath, parent)

    def register_handlers(self) -> None:
        super().register_handlers()

    def load(self) -> None:
        super().load()
        self.load_children()

    def load_children(self) -> dict:
        self.log.debug('loading children objects')
        self.children = self._load_children()
        self.log.debug(f'loaded {len(self.children)} children objects')
        return self.children
        
    def _load_children(self) -> dict:
        rtn = self.util.paths.getFiles(self.filepath)
        for nm, val in rtn.items():
            self.log.debug(f'    {nm}')
        return rtn


class sjoObjectsChildren():
    children:dict
    event:sjuEvent
    paths:sjuPath
    log:sjuLog
    childtype:str
    
    def __init__(self, parent:object) -> None:
        self.parent = parent 
        self.log = parent.log
        self.event = parent.event
        self.paths = parent.paths
        self.childtype = type(self).__name__
        self.log.info('class instantiated')  

    def load(self, folderpath:Path, childtype:object ):
        self.log.info(f'started loading children {childtype.__name__}')
        self.log.info(f'completed loading children {childtype.__name__}')
        self.event.broadcast(f'{self.parent.eventprefix}')

    def set_item(self, objchild:object):
        self.children[objchild.name] = objchild
        self.log.info(f'child {objchild.type}.{objchild.name} assigned to {self.parent.name}')
        self.event.broadcast('%s.%s.changed' %(self.parent.eventprefix, self.__name__), self.event.pack_data(self.parent, change='set_item') )

    def load(self, folderpath:Path, childtype:object ):
        self.log.info(f'started loading children {childtype.__name__}')
        self.log.info(f'completed loading children {childtype.__name__}')
        self.event.broadcast(f'{self.parent.eventprefix}')

    def updatecheck_allchildren(self):
        self.log.info(f'prompting all {self.childtype} to reload')
        # loop thru all children and prompt them to initiate an update check
        pass

    def save_all(self):
        self.log.info(f'prompting all {self.childtype} to reload')
        # loop thru all children and prompt them to save 
        pass 

    def reload_all(self):
        self.log.info(f'prompting all {self.childtype} to reload')
        # loop thru all children and prompt them to reload
        pass 

    


if __name__=='__main__':
    util = sjuUtil()
    obj = sjoObjectsBase(util, Path(r"C:\git\sqljin\configs\organizations\Teradata\Collections\Metrics"))
    obj.load()
    obj.variables.default = {"version":0, "variables":{"something":"Awesome!!!"}}
    # obj.variables.add()