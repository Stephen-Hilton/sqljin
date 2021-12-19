# ######################################################
#
# build factory for all config structures
#
# ######################################################

from pathlib import Path
import sys 

from .sj_event import sj_Event
from .sj_logger import sj_Logger
from .sj_paths import sj_Paths

class sj_Config():
    name: str = ''
    configdb_filepath: Path 

    event: sj_Event
    log: sj_Logger
    paths: sj_Paths


    def __init__(self, sj_event:sj_Event, name:str, configdb_filepath:Path ) -> None:
        self.event = sj_event
        self.log = sj_event.log
        self.paths = sj_event.log.paths
        self.name = name 
        self.configdb_filepath = configdb_filepath
        self.log.info(f'Config Added: {name}')



class sj_Config_Factory():
    configs: dict = {}

    def __init__(self, sj_event: sj_Event) -> None:
        self.event = sj_event
        self.log = sj_event.log
        self.path = sj_event.log.paths
        self.configs = {}
        self.log.debug('Config Factory Instantiated')

        # add events handled:
        self.event.add_handler("get.config", self.add_config)

    def add_config(self, name:str, configdb_filepath:Path ):
        newconfig = sj_Config(self.event, name, configdb_filepath)
        self.configs[name] = newconfig
        

        return newconfig

    def confirm_unique_orgid(self) -> bool:
        pass 

    def load_configdb(self, sj_config: sj_Config):
        pass


