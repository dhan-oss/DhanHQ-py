from enum import Enum

class OrderType(Enum):
    LIMIT = "For Limit Order types"
    MARKET = "For market Order types"
    STOP_LOSS = "For Stop Loss Limit orders"
    STOP_LOSS_MARKET = "For Stop Loss Market orders"

    @property
    def description(self):
        return self.value
