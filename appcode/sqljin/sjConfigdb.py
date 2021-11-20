# ######################################################
#
# build functions for managing config.db interactions
#
# ######################################################

import sqlite3
from sqlite3 import Error
from pathlib import Path
from sqlite3.dbapi2 import Connection


configdb = 'config.db'

def connect_configdb(dbfilepath: Path, create_if_missing:bool = False) -> object:
    """create a connection to the config.db """
    conn = None
    try:
        if dbfilepath.exists or create_if_missing:
            conn = sqlite3.connect(dbfilepath)
            broadcast('log','connected to %s (sqlite version %s)' %(dbfilepath, sqlite3.version))
            return conn 
        else:
            return str('%s file does not exist' %dbfilepath.absolute())

    except Error as e:
        broadcast('log.error', 'error during login attempt to %s, error: %s' %(dbfilepath, str(e)))
        return str('error during login attempt to %s, error: %s' %(dbfilepath, str(e)))



def validate_configdb(orgPath:Path) -> str:
    """validates whether the configdb exists, and is well structured"""
    if not Path(orgPath / configdb ).exists(): 
        broadcast('log','configdb for %s is missing' %orgPath.name)
        return 'file missing'
    else:
        pass
    


def add_configdb(orgPath:Path):
    """adds a new config.db in the supplied Org folder, with correct data structures"""
    broadcast('log.info', 'add new configdb, with correct table structures')
    conn = connect_configdb(Path(orgPath / configdb))
    if type(conn) == sqlite3.Connection:
        pass
        

    

if __name__ == '__main__':
    add_configdb( Path('C:'/'git'/'sqljin'/'configs'/'Teradata') )
