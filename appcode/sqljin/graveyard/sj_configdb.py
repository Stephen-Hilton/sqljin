# ######################################################
#
# build functions for managing config.db interactions
#
# ######################################################

import sqlite3
from pathlib import Path
import sys 

# from dbConn.dbconn_sqlite import dbConn_SQLite as dbsqlite
# from configs.Global.plugins.dbConn.dbconn_sqlite import dbConn_SQLite as dbsqlite
from ..util.sj_event import sj_Event
from ..util.sj_logger import sj_Logger
from ..util.sj_paths import sj_Paths


class sj_Config():
    configdb: object
    log: sj_Logger
    paths: sj_Paths

    def __init__(self, sj_event:sj_Event, configname:str, orgid:int) -> None:
        self.event = sj_event
        self.log = sj_event.log
        self.paths = sj_event.log.paths
        self.configname = configname
        self.orgid = orgid
        self.configfilepath = Path(self.paths.configPath / configname / 'config.db')
        from configs.Global.plugins.dbConn.dbconn_sqlite import dbConn_SQLite as dbsqlite


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
        db.execute(self.sql_create_table_tsystems())
        db.execute(self.sql_insert('tsystems', {'ID':1, 'Name':'TestDB', 'Host':'some.url', 'StartTS':'2021-11-01 23:59:59'}))
        db.execute(self.sql_insert('tsystems', {'ID':1, 'Name':'TestDB', 'Host':'some.new.url'}))
        db.execute(self.sql_insert('tsystems', {'ID':2, 'Name':'anotherDB', 'Host':'someother.url'}))
        db.execute(self.sql_create_view('tsystems'))

        db.execute(self.sql_create_table_tcredentials())
        db.execute(self.sql_insert('tcredentials', {'ID':1, 'UserName':'Sample', 'Password':'something_old', 'StartTS':'2021-11-01 23:59:59'}))
        db.execute(self.sql_insert('tcredentials', {'ID':1, 'UserName':'Sample', 'Password':'something_new_and_secure'}))
        db.execute(self.sql_create_view('tcredentials'))

        db.execute(self.sql_create_table_tvartypes())
        db.execute(self.sql_insert('tvartypes', {'ID':1, 'Order':1, 'Name':'Override'}))
        db.execute(self.sql_insert('tvartypes', {'ID':2, 'Order':2, 'Name':'Job/System'}))
        db.execute(self.sql_insert('tvartypes', {'ID':3, 'Order':3, 'Name':'System'}))
        db.execute(self.sql_insert('tvartypes', {'ID':4, 'Order':4, 'Name':'Job'}))
        db.execute(self.sql_insert('tvartypes', {'ID':5, 'Order':5, 'Name':'Collection'}))
        db.execute(self.sql_insert('tvartypes', {'ID':6, 'Order':6, 'Name':'Organization'}))
        db.execute(self.sql_insert('tvartypes', {'ID':7, 'Order':7, 'Name':'Global'}))
        db.execute(self.sql_create_view('tvartypes'))

        db.commit()
        rtn = db.execute('select * from tvartypes')

        


    def repair(self):
        """repair config.db to proper structure without losing data (TBD)"""
        pass 


    def sql_create_table_tsystems(self):
        sql = """
        CREATE TABLE IF NOT EXISTS  tsystems 
        (ID      int 
        ,OrgID   int
        ,ProxyID int  
        ,Name    text
        ,Host    text
        ,LogMech text
        ,Encrypt int
        ,CredID  int
        ,IconURL text
        ,StartTS text  DATETIME DEFAULT CURRENT_TIMESTAMP
        ,PRIMARY KEY (ID, OrgID, StartTS)
        );"""
        return sql

    def sql_create_table_tcredentials(self):
        sql = """
        CREATE TABLE IF NOT EXISTS  tcredentials
        (ID       int 
        ,OrgID    int
        ,UserName text
        ,Password text
        ,Token    text
        ,StartTS text  DATETIME DEFAULT CURRENT_TIMESTAMP
        ,PRIMARY KEY (ID, OrgID, StartTS)
        );"""
        return sql

    def sql_create_table_tvartypes(self):
        sql = """
        CREATE TABLE IF NOT EXISTS  tvartypes
        (ID      int 
        ,Name    text
        ,'Order' text
        ,StartTS text  DATETIME DEFAULT CURRENT_TIMESTAMP
        ,PRIMARY KEY (ID, StartTS)
        );"""
        return sql


    def sql_create_table_tvariables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS  tvariables
        (ID      int
        ,OrgID   int 
        ,VarTypeID int
        ,VarOwnerID int
        ,Name    text
        ,Value   text
        ,Type    text
        ,StartTS text  DATETIME DEFAULT CURRENT_TIMESTAMP
        ,PRIMARY KEY (ID, OrgID, StartTS, VarTypeID, VarOwnerID)
        );"""
        return sql

        
    @staticmethod
    def get_column_list(tablename):
        if tablename == 'tsystems': 
            return ["ID", "OrgID", "ProxyID", "Name", "Host", "LogMech", "Encrypt", "CredID", "IconURL", "StartTS"]
        if tablename == 'tcredentials': 
            return ["ID", "OrgID", "UserName", "Password", "Token", "StartTS"]    
        if tablename == 'tvartypes':
            return ["ID", "Name", "Order", "StartTS"]
        if tablename == 'tvariables':
            return ["ID", "OrgID", "VarTypeID", "VarOwnerID", "Name", "Value", "Type", "StartTS"]
            




    def sql_create_view(self, tablename):
        sql = f"""
        CREATE VIEW IF NOT EXISTS  {tablename[1:]}  as
            Select t.* 
            from {tablename} as t 
            join (select ID, OrgID, max(StartTS) as StartTS_Max 
                from {tablename} group by ID) as mx
             on t.ID = mx.ID 
            and t.OrgID = m.OrgID
            and t.StartTS = StartTS_Max
        ;"""
        return sql
    
    def sql_insert(self, tablename:str, rowdata:dict={}):
        columns =  [c for c in self.get_column_list(tablename) ]
        cols = []
        vals = [] 
        for colname, celldata in rowdata.items():
            if colname in columns:
                cols.append(f"'{colname}'")
                datmod = str(celldata) if str(celldata).isnumeric() else "'%s'" %str(celldata).replace("'","''")
                vals.append(datmod)

        # explicitly add special defaults
        if "'ID'" not in cols:  
            cols.append("'ID'")
            vals.append( f"(SELECT MAX(ID) + 1 FROM {tablename})" )
        if "'OrgID'" not in cols and 'OrgID' in columns:
            cols.append("'OrgID'")
            vals.append( f'{self.orgid}')

        columns = ','.join(cols)
        values = ','.join(vals)
        sql = f'INSERT INTO {tablename} ({columns}) VALUES ({values});'
        return sql 


            
            




            
            


        


