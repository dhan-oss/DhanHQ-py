from enum import Enum

class Validity(Enum):
    DAY = "Valid till end of day"
    IOC = "Immediate or Cancel"

    @property
    def description(self):
        return self.value
