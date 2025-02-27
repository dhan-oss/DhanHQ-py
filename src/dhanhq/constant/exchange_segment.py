from enum import Enum

from .exchange import Exchange
from .segment import Segment


class ExchangeSegment(Enum):
    IDX_I = (Exchange.IDX, Segment.I, 0)
    NSE_EQ = (Exchange.NSE, Segment.EQ, 1)
    NSE_FNO = (Exchange.NSE, Segment.FNO, 2)
    NSE_CURRENCY = (Exchange.NSE, Segment.CURRENCY, 3)
    BSE_EQ = (Exchange.BSE, Segment.EQ, 4)
    BSE_FNO = (Exchange.BSE, Segment.FNO, 8)
    BSE_CURRENCY = (Exchange.BSE, Segment.CURRENCY, 7)
    MCX_COMM = (Exchange.MCX, Segment.COMM, 5)

    @property
    def exchange(self):
        return self.value[0]

    @property
    def segment(self):
        return self.value[1]

    @property
    def code(self):
        return self.value[2]
