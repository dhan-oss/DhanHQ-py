from enum import Enum

class TransactionType(Enum):
    BUY = "Buy"
    SELL = "Sell"

    @property
    def description(self):
        return self.value
