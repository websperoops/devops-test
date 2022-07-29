from enum import Enum

class BaseEnum(Enum):

    def __str__(self):
        return str(self.value)
    
    def __int__(self):
        return int(self.value)