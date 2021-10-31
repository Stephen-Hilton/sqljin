from pathlib import Path 
from dataclasses import dataclass


@dataclass
class sjconfig():
    log: object
    paths: object 

    def __init__(self, paths:object, logger:object):
        self.log = logger
        self.paths = paths
        self.log.info('sjconfig class instantiated')

    def load_manifest(self):
        self.log.info('loading manifest from ')

