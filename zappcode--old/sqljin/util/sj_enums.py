from enum import Enum, auto
import enum 

class RETURN_STATUS(Enum):
    SUCCESS = auto()
    WARNING_GENERAL = auto()
    WARNING_DUPLICATE = auto()
    ERROR_CRITICAL = auto()
