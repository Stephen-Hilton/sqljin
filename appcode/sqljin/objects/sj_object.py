# ######################################################
#
# object class for all object.Properties
#
# ######################################################

from pathlib import Path

import dbConn.dbconn_sqlite as dbConnSQLite

import util.sj_event  as sjevent
import util.sj_logger as sjlog
import util.sj_paths  as sjpaths

import objects.sj_datamgr  as sjdatamgr  
import objects.sj_property as sjprop  
import objects.sj_object   as sjobject  
import objects.sj_orgs     as sjorg



class sj_Object():

    props_active = []
    props_variables = []
    props_history = []

    id: int 
    objecttype: str
    instancename: str 
    active: bool
    parentOrg: object # sjorg.sj_Org

    def __init__(self, utils:dict) -> None:
        self.event = utils['event']
        self.log   = utils['log']
        self.paths = utils['paths']
        self.utils = utils 

