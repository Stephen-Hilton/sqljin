# plugin style load:
# dbconn_mod ='dbconn_sqlite'
# dbconn_filePath = str(Path(self.paths.appdbConnPath / Path(dbconn_mod + '.py')))
# self.log.debug(f'attempting to load plugin: {dbconn_filePath}')
# dbconnSQLite_spec = importlib.util.spec_from_file_location(dbconn_mod, dbconn_filePath)
# dbconnSQLite_plugin = importlib.util.module_from_spec(dbconnSQLite_spec)
# dbconnSQLite_spec.loader.exec_module(dbconnSQLite_plugin)
# self.dbConn = dbconnSQLite_plugin.dbConn_SQLite(self.log, systemname=f'app specific ({self.paths.appname}) SQLite', host=self.configdb_filepath)
from datetime import datetime
from locale import format_string
from pathlib import Path
from dateutil.parser import parse
import validators

now = datetime.now()
print(now)

dtstrings = ['2021-12-17', '12/17/2021', '12/17/21', '2021/12/17', '12/17/21 3:45:00 pm']
for dtstr in dtstrings:
    pass 
    # print(f"original: {dtstr}  \t TIME adjusted: {parse(dtstr).strftime('%Y-%m-%d %H:%M:%S')}" )

test = str(float('122.3335534'))
print(test, type(test))

