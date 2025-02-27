from enum import Enum

class InstrumentType(Enum):
    INDEX = "Index"
    FUTIDX = "Futures of Index"
    OPTIDX = "Options of Index"
    EQUITY = "Equity"
    FUTSTK = "Futures of Stock"
    OPTSTK = "Options of Stock"
    FUTCOM = "Futures of Commodity"
    OPTFUT = "Options of Commodity Futures"
    FUTCUR = "Futures of Currency"
    OPTCUR = "Options of Currency"

    @property
    def description(self):
        return self.value