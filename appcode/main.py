import sys 
from sqljin.sjuUtil import sjuUtil
from sqljin.sjoGlobal import sjoGlobal

# start all utilities:
util = sjuUtil()

# TODO: update all contents

# load all model objects:
util.log.header(f'Loading Model Objects')
sjglobal = sjoGlobal(util)


# start GUI specified
# TODO:

util.log.header('APPLICATION COMPLETE')