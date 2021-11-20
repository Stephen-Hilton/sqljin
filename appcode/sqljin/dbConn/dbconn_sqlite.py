# ######################################################
#
# build functions for managing config.db interactions
#
# ######################################################
import logging
import sqlite3
import dbconn_base
import pandas as pd

class dbConn_SQLite(dbconn_base.dbConn_Base):

    def _connect_(self) -> bool:
        try:
            self.connection = sqlite3.connect(self.host)
            self.cursor = self.connection.cursor
            return True
        except Exception as e:
            self.log.error('error during connection: %s' %str(e))
            return False

    def _commit_(self) -> bool:
        try:
            self.connection.commit()
            return True
        except Exception as e:
            self.log.error('error during commit: %s' %str(e))    
            return False

    def _execute_(self, sql) -> tuple:
        try:
            df = pd.read_sql_query(sql, self.connection)
            return (len(df.index), df)
        except Exception as e:
            self.log.error('error during execution: %s' %str(e))
            return None
    
    def _disconnect_(self) -> bool:
        try:
            self.connection.close()
            return True
        except Exception as e:
            self.log.error('error during disconnect: %s' %str(e))
            return False 

    def _rollback_(self) -> bool:
        try:
            self.connection.rollback()
            return False
        except Exception as e:
            self.log.error('error during rollback: %s' %str(e))
            return False

    




# in script testing:
if __name__ == '__main__':

    # setup test logging...
    log = logging.Logger(__name__)
    shandler = logging.StreamHandler()
    shandler.setLevel(logging.DEBUG)
    log.addHandler(shandler)

    testdb = dbConn_SQLite( log, 
                            systemname= 'sqlite3_test', 
                            host='C:/git/sqljin/appcode/sqljin/test.db' )
    log.info(str(testdb))
    testdb.connect()
    testdb.execute('create table x (col1 char)')
    testdb.disconnect()