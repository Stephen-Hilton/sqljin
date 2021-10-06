from enum import Enum 

# define enums
class runStatus(Enum):
    NOTSTARTED = 0
    PREWORK    = 10
    RUNNING    = 20
    WAITING    = 30
    PAUSED     = 40
    POSTWORK   = 50
    ERROR      = 99
    
class runType(Enum):
    DIRECT = 10
    BTEQ = 20
    PYTHON = 30
    SQLFILE = 40
    
class taskType(Enum):  # export, execute, checkpoint, script, chart, import, etc.
    NOTSTARTED = 0
    EXECUTE = 10
    EXPORT  = 20
    IMPORT  = 30
    SCRIPT  = 40
    CHART   = 50
    CHECKPOINT = 80
    COMPLETE = 90
    ERROR = 99