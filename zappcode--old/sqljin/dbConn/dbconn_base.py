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
    autocommit_default = None

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

    def connected(self) ->bool:
        self.log.info(f'testing connection to {self.systemname}')
        rtn = self._connected_()
        self.log.info( 'connected!' if rtn else 'not connected' )
        return rtn

    def _connected_(self) ->bool:
        return False if self.execute('select 1','scalar') is None else True

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
    def execute(self, sql='', datareturned='none', autocommit=None, savepath:Path = None, logsql=True) -> tuple:
        """
        Executes supplied SQL and returns tuple of (row count, return structure|None, list of column names|None)
        If failure, returns None
        """

        # define autocommit setting 
        if self.autocommit_default is not None and autocommit is None:
            autocommit = self.autocommit_default
        if autocommit is None: autocommit = False

        # connect if not
        if self.connection is None: self.connect()
        if logsql: self.log.info('attempting to execute sql:%s' %self.logformat_sql(sql))
        
        # call core execute method (overriden)
        rtn = self._execute_(sql)

        # determine success
        if rtn is None:
            self.log.error('execution failed')
            # behavior of failed SQL is handled further up the stack
            return None 
        else:
            # build return object:
            rows = rtn[1]  # TODO: either rows returned, or if zero, rows affected
            df = pd.DataFrame(rtn[0])
            df.columns = [col.lower() for col in list(df.columns)] # why lower?  

            if logsql: self.log.info('execution complete (%i rows)' %rows)
            if autocommit: self.commit()


            try:
                if   datareturned.lower() == 'none': datartn = None
                elif datareturned in ['df','dataframe','data','pandas']:  datartn = df
                elif datareturned in ['scalar','single','first']: datartn = df.iloc[0,0]
                elif datareturned in ['dict', 'dictcol']:  datartn = df.to_dict() 
                elif datareturned in ['dictrow','list']:  
                    datartn = df.to_dict('records')
                elif datareturned == 'json':  datartn = df.to_json()
                elif datareturned in ['str','string','cli']:   datartn = df.to_string()
                elif datareturned == 'csv':   datartn = df.to_csv(na_rep = '', index = False)  
                elif datareturned == 'html':  datartn = df.to_html()
                elif datareturned == 'pickle': datartn = df.to_pickle(savepath)
                else:
                    self.log.warning("""data return requested (%s) is not supported.
                    Currently supported types: [dataframe/df/data, dict, list, json, str/string/cli, csv, html, json]
                    For now, returning a dataframe, and you''ll like it.""" %datareturned)
                if savepath and datareturned != 'pickle':
                    with open( Path(savepath).resolve(),'w') as fh:
                        fh.write(str(datartn))
            except Exception as e:
                self.log.exception(f"data returned doesn't match data return requested ({datareturned}), returning None")
                datartn = None

            rtndict = {"data":datartn, "rows":rows, "columns": list(df.columns)}
            if savepath: rtndict["path"] = savepath.resolve()
            return rtndict
            

    def _execute_(self, sql) -> tuple:
        # TODO: implement execution logic, always returned as a tuple of (dataframe, int)
        rows = 4
        dfReturn = pd.DataFrame({'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']})
        return (dfReturn, rows)

    def commit(self, logsql=True) -> bool:
        if logsql: self.log.debug(f'attempting to commit changes to {self.systemname} ({self.classname})...')
        rtn = self._commit_()
        if rtn:
            if logsql: self.log.info('changes committed')
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