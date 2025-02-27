from enum import Enum

class ProductType(Enum):
    CNC = "Cash & Carry for equity deliveries"
    INTRADAY = "Intraday for Equity, Futures & Options"
    MARGIN = "Carry Forward in Futures & Options"
    CO = "Cover Order; entry and stop loss for Intraday"
    BO = "Bracket Order; entry, stop loss & target price for Intraday"
    MTF = "Margin Traded Fund"

    @property
    def description(self):
        return self.value
