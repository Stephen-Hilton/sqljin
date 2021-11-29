from pathlib import Path
from datetime import datetime
import logging



# testing:
if __name__ == '__main__':
    
    add_handler('log.test', log.debug )
    add_handler('log.test', log.info )
    add_handler('log.test', log.warning )
