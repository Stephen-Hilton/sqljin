from pathlib import Path 
from dataclasses import dataclass
# from sjLog import sjlog
# from sjPath import sjpath
# from sjEvent import sjevent

@dataclass
class sjupdate():
    log:   object # sjlog
    paths: object # sjpath 
    event: object # sjevent 

    def __init__(self, logger:object, paths:object, events:object):
        self.log = logger
        self.paths = paths
        self.event = events
        self.log.info('sjupdate class instantiated')


    def update_from_source(self):
        for org in ['Global','Teradata','Wipro']:    
            self.log.info(f'org {org}: Preparing to update all files from source masters')
            self.log.info(f'org {org}: Gathering all local versions')
            self.log.info(f'org {org}: Downloading source manifests for remote versions')
            self.log.info(f'org {org}: Comparing local versions to remote source versions, and building update list')
            self.log.info(f'org {org}: Updating all needed files')
            for x in range(1,5):
                self.log.debug(f'org {org}: downloading file %i from source: abc' %x )
                self.log.debug(f'org {org}: Running validation test to ensure successful file transfer')
            self.log.info(f'org {org}: Update complete!')
            

