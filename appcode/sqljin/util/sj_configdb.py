# ######################################################
#
# build functions for managing config.db interactions
#
# ######################################################

import sqlite3
from pathlib import Path
import sys 

sys.path.append("..") # to allow imports of dbConn modules
from dbConn.dbconn_sqlite import dbConn_SQLite as dbsqlite
from .sj_event import sj_Event
from .sj_logger import sj_Logger
from .sj_paths import sj_Paths

class sj_Config():
    configdb: dbsqlite
    log: sj_Logger
    paths: sj_Paths

    def __init__(self, sj_event:sj_Event, configname:str) -> None:
        self.event = sj_event
        self.log = sj_event.log
        self.paths = sj_event.log.paths
        self.configname = configname
        self.configfilepath = Path(self.paths.configPath / configname / 'config.db')

        # connect to config.db
        self.log.info(f'reading config: {configname} from path: {self.configfilepath}')
        config_exists = self.configfilepath.exists()
        self.configdb = dbsqlite(self.log, 'Local', self.configfilepath)
        self.configdb.connect()

        if not config_exists: self.new_configdb()

        self.load()
        return None


    def load(self):
        """load core data from config.db into object"""
        pass

    def new_configdb(self):
        """add all required tables to a newly created config.db"""
        self.log.warning(f'building new config table structures in {self.configname}/config.db')
        
        db = self.configdb
        rtn = db.execute(self.sql_create_systems(),autocommit=True)
        rtn = db.execute(self.sql_insert('systems',
                                [{'Name':'TestDB','Host':'some.url'},
                                {'Name':'anotherDB','Host':'someother.url'}]), autocommit=True)
        


    def repair(self):
        """repair config.db to proper structure without losing data (TBD)"""
        pass 


    def sql_create_systems(self):
        sql = """
        CREATE TABLE IF NOT EXISTS  systems 
        (ID      int 
        ,ProxyID int   DEFAULT 0
        ,Name    text
        ,Host    text
        ,LogMech text
        ,Encrypt int
        ,IconURL text
        ,StartTS text  DATETIME DEFAULT CURRENT_TIMESTAMP
        ,PRIMARY KEY (ID, StartTS)
        );"""
        return sql

    
    def sql_insert(self, tablename:str, insert_rows:list=[]):
        cols =  [c for c in self.get_column_list(tablename) if c != "StartTS"]
        valInsert = []
        valdict = {}
        for valdict in insert_rows:  # for all rows supplied to be inserted
            vals = []
            for col in cols:           # look thru expected insert values
                if col not in valdict:   # if column is missing
                    if col == "ID":        # ID gets special treatment:
                        valdict[col] = f"(SELECT MAX(ID) + 1 FROM {tablename})"
                    else:                         
                        valdict[col] = 'NULL'  # everything else gets NULL
                    vals.append("%s" %valdict[col])  # don't wrap as string if just defined
                else:    
                    vals.append("'%s'" %valdict[col])  # wrap as string if exists
            valInsert.append( ','.join(vals) )
        columns = ','.join([col for col in cols])
        values = '),\n('.join( [val for val in valInsert] )
        sql = f'INSERT INTO {tablename} ({columns}) VALUES \n({values});'
        return sql 

        
    @staticmethod
    def get_column_list(tablename):
        if tablename == 'systems': 
            return ["ID", "ProxyID", "Name", "Host", "LogMech", "Encrypt", "IconURL", "StartTS"]

            
            




            
            


        


