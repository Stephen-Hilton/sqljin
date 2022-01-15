from pathlib import Path
import importlib
import sys

try:
    from .sj_orgs import sj_Org
except:
    pass

from ..util.sj_event import sj_Event
from ..util.sj_logger import sj_Logger
from ..util.sj_paths import sj_Paths

class sj_System():
    name: str = ''
    driver: Path = ''
    host: str = ''
    encrypt: bool = False
    logmech: str = ''
    credentials_id: int = None
    credentials: dict = None
     
    event: sj_Event
    log: sj_Logger
    paths: sj_Paths
    # org: sj_Org

    def __init__(self, parentorg:object, sysobj:list =[] ) -> None:
        self.log = parentorg.log
        self.event = parentorg.event
        self.paths = parentorg.paths
        self.org = parentorg

        if sysobj == []:
            self.log.error(f'incomplete data provided for creation of system: {sysobj}')
        else:
            self.name = sysobj['instance']
            self.log.info(f'New ')
            if 'driver'   in sysobj: self.driver   = Path(sysobj['driver'])
            if 'host'     in sysobj: self.host     = sysobj['host']
            if 'encrypt'  in sysobj: self.encrypt  = sysobj['encrypt']
            if 'logmech'  in sysobj: self.logmech  = sysobj['logmech']
            if 'credentials_id' in sysobj: self.credentials_id = sysobj['credentials_id']

    def get_credentials(self):
        if not self.credentials_id:
            self.log.error(f'no credentials defined for system {self.name}')
        else:
            self.log.debug(f'retrieving linked credential object')
            self.org.get_object_properties(self.credentials_id,'credentials_id')