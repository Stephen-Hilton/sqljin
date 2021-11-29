# ######################################################
#
# BASE CLASS for dbConn_Connections 
#  inheriting this class is required for SQLJin to
#  recognize and import correctly.  
#  
#  core methods call another method of the same name
#  but prefixed of underscore (_) which contains all
#  core functionality.  This allows extensions to leave
#  setup / logging / tear-down from parent class, and 
#  simply override the core functionality
#   
# To-Do:  Move DB work to own thread
#
# ######################################################

import logging
import pandas as pd 
from pathlib import Path
from pandas.io import json

class dbConn_Base():
    systemname:str = ''
    username:str = ''
    password:str = ''
    host:str = ''
    logmech:str = ''
    encrypt:bool = False 

    log:logging.Logger = None 
    classname:str = ''
    connection:object = None 
    cursor:object = None


    def __init__(self, logger:logging.Logger, systemname='', host='', username='', password='', logmech='', encrypt=False) -> None:
        self.log = logger

        self.systemname = 'not set' if systemname == '' else systemname  
        self.host       = 'not set' if host       == '' else host        
        self.username   = 'not set' if username   == '' else username    
        self.password   = 'not set' if password   == '' else password    
        self.logmech    = 'not set' if logmech    == '' else logmech     
        self.encrypt = encrypt
        self.classname = str(self.__class__)
        self.connection = None

        self.log.debug('instantiated class: %s  for use by system: %s' %(self.classname, self.systemname))
        return None 

    def masked_password(self) -> str:
        return '*' * len(self.password)

    def logformat_sql(self, sql) -> str:
        brk = '\n    %s\n' %str('-'*40)
        return brk + '\n'.join('    %s' %l for l in sql.strip().split('\n') ) + brk

    def __str__(self) -> str:
        rtn = ['Database Connection Class: %s ' %self.classname]
        rtn.append(f'  for System:  {self.systemname} ')
        rtn.append(f'        Host:  {self.host} ')
        rtn.append(f'    UserName:  {self.username} ')
        rtn.append(f'    Password:  {self.masked_password()} ')
        rtn.append(f'  Login Mech:  {self.logmech} ')
        rtn.append(f'  Encrypted?:  {self.encrypt} ')
        return '\n'.join(rtn)

    # CONNECTION LOGIC:
    # ----------------------------------------------
    def connect(self, host='', username='', password='', logmech='') -> bool:
        # make sure class has up-to-date information
        if host     != '': self.host     = host        
        if username != '': self.username = username    
        if password != '': self.password = password    
        if logmech  != '': self.logmech  = logmech  
        self.connection = None 

        # connect to the system in question:
        self.log.info(f'attempting connection to {self.systemname} ({self.classname})...')
        rtn = self._connect_()
        if rtn:
            self.log.info('connection successful!')
        else:
            self.log.error('connection failed')
        return rtn 

    def _connect_(self) -> bool:
        """core connection logic.  this is wrapped by the db.connect() function, which provides parameter setup and logging.
        There are not paremeters, all variables are available at the class level (self.)
        Returns: boolean, True if connection succeeds, False if it fails. 
        Note: implementers are encouraged to add more error handling and logging of issues"""
        # TODO: define specific error types 
        # TODO: implement database connection logic
        self.connection = None # actually, database connection object
        return True  # or False

    def disconnect(self) -> bool:
        self.log.info(f'disconnecting from {self.systemname} ({self.classname})...')
        rtn = self._disconnect_()
        if rtn:
            self.log.info('disconnected from database')
        else:
            self.log.error('error disconnecting from database, destroying program object')
            self.connection = None 
        return rtn

    def _disconnect_(self) -> bool:
        # TODO: implement database disconnection logic
        return True # or False



    # SQL EXECUTION LOGIC
    # ----------------------------------------------
    def execute(self, sql='', datareturned='none', savepath:Path = None, autocommit=False) -> tuple:
        """return tuple of (rows_affected/returned, dataframe/None)"""
        if self.connection == None: self.connect()
        self.log.info('attempting to execute sql:%s' %self.logformat_sql(sql))
        rtn = self._execute_(sql)

        if rtn is None:
            self.log.error('execution failed')
            return None
        else:
            self.log.info('execution complete (%i rows)' %rtn[0])
            if autocommit: self.commit()

            # build return object:
            rows = rtn[0]
            df = pd.DataFrame(rtn[1])

            if   datareturned == 'none': return (rows, None)
            elif datareturned in ['df','dataframe','data','pandas']:  rtn = df
            elif datareturned == 'dict':  rtn = df.to_dict() 
            elif datareturned == 'json':  rtn = df.to_json()
            elif datareturned in ['str','string','cli']:   rtn = df.to_string()
            elif datareturned == 'csv':   rtn = df.to_csv(na_rep = '', index = False)  
            elif datareturned == 'html':  rtn = df.to_html()
            elif datareturned == 'pickle': rtn = df.to_pickle(savepath)
            elif datareturned == 'list':  
                rtn = df.to_dict() 
                rtn2 = []
                for k in rtn.keys():
                    rtn2.append([k, [x for x in rtn[k].values()]] )
                rtn = rtn2 
            else:
                self.log.warning("""data return requested (%s) is not supported.
                Currently supported types: [dataframe/df/data, dict, list, json, str/string/cli, csv, html, json]
                For now, returning a dataframe, and you''ll like it.""" %datareturned)
            if savepath and datareturned != 'pickle':
                with open( Path(savepath).resolve(),'w') as fh:
                    fh.write(str(rtn))
            return (rows, rtn)
            

    def _execute_(self, sql) -> tuple:
        # TODO: implement execution logic, always returned as a tuple of (int, dict)
        rows = 4
        dfReturn = pd.DataFrame({'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']})
        return (rows, dfReturn)

    def commit(self) -> bool:
        self.log.debug(f'attempting to commit changes to {self.systemname} ({self.classname})...')
        rtn = self._commit_()
        if rtn:
            self.log.info('changes committed')
        else:
            self.log.error('error while committing changes')
        return rtn

    def _commit_(self) -> bool:
        # TODO: implement database commit logic
        return True # or False

    def rollback(self) -> bool:
        self.log.debug(f'attempting to roll-back changes to {self.systemname} ({self.classname})...')
        rtn = self._rollback_()
        if rtn:
            self.log.info('changes discarded / rolled back')
        else:
            self.log.error('error while rolling back changes')
        return rtn

    def _rollback_(self) -> bool:
        # TODO: implement database commit logic
        return True # or False





# in script testing:
if __name__ == '__main__':

    # setup test logging...
    log = logging.Logger(__name__)
    shandler = logging.StreamHandler()
    shandler.setLevel(logging.DEBUG)
    log.addHandler(shandler)

    testdb = dbConn_Base( log, 
                            systemname= 'Big Ol Test System', 
                            host='somehost', 
                            username='stephen', 
                            password='poopypants', 
                            logmech='default', 
                            encrypt=False)
    log.info(str(testdb))
    testdb.connect()
    log.info( testdb.execute('select * from stuff', 'dict') )

    testdb.execute('select * from stuff', 'html', Path('C:/git/sqljin/appcode/sqljin/test.out')) 
    testdb.execute("""
select
 stuff
,things
,junk
,trash
from garbage
where fun='no';
    """
    )
    testdb.disconnect()