from enum import Enum

class Segment(Enum):
    I = "Index value"
    EQ = "Equity"
    FNO = "Futures and Options"
    CURRENCY = "Commodity"
    COMM = "Currency"

    @property
    def description(self):
        return self.value
