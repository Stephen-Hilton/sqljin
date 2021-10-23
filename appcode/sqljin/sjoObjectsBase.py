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
    children: dict

    def __init__(self, util: sjuUtil, filepath: Path, parent: object = None):
        super().__init__(util, filepath, parent)

    def register_handlers(self) -> None:
        event = self.util.event
        prefix = self.prefix.strip()[:-1]
        super().register_handlers()
        event.add_handler(prefix + '.addnew_child', self.addnew_child)
        event.add_handler(prefix + '.delete_child', self.delete_child)

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

    def addnew_child(self, name:str, *args, **kwargs ) -> object:
        self.log.info(f'Add new child: {name}')
        self.children[name] = self._addnew_child
        self.log.debug(f'child added: {name}')

    def _addnew_child(self, name:str) -> object:
        return {'new child', object}

    def delete_child(self, name:str, *args, **kwargs ) -> None:
        self.log.warning(f'Remove child: {name}')
        if not name in self.children: 
            self.log.warning(f'The child {name} does not exist as a child, skipping')
        else:
            if self._delete_child: 
                del self.children[name]
            self.log.debug(f'child removed: {name}')

    def _delete_child(self, name:str) -> bool:
        return False
          
        


if __name__=='__main__':
    util = sjuUtil()
    obj = sjoObjectsBase(util, Path(r"C:\git\sqljin\configs\organizations\Teradata\Collections\Metrics"))
    obj.load()
    obj.variables.default = {"version":0, "variables":{"something":"Awesome!!!"}}
    # obj.variables.add()