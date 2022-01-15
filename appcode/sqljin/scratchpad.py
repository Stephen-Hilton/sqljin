# plugin style load:
# dbconn_mod ='dbconn_sqlite'
# dbconn_filePath = str(Path(self.paths.appdbConnPath / Path(dbconn_mod + '.py')))
# self.log.debug(f'attempting to load plugin: {dbconn_filePath}')
# dbconnSQLite_spec = importlib.util.spec_from_file_location(dbconn_mod, dbconn_filePath)
# dbconnSQLite_plugin = importlib.util.module_from_spec(dbconnSQLite_spec)
# dbconnSQLite_spec.loader.exec_module(dbconnSQLite_plugin)
# self.dbConn = dbconnSQLite_plugin.dbConn_SQLite(self.log, systemname=f'app specific ({self.paths.appname}) SQLite', host=self.configdb_filepath)
