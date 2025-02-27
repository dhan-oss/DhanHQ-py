from enum import Enum

class Exchange(Enum):
    IDX = "Index"
    NSE = "National Stock Exchange"
    BSE = "Bombay Stock Exchange"
    MCX = "Multi Commodity Exchange"
    ALL = "All Exchanges - NSE, BSE, MCX"

    @property
    def description(self):
        return self.value
