from enum import Enum

class PositionType(Enum):
    LONG = "When net bought quantity is more than sold quantity"
    SHORT = "When net sold quantity is more than bought quantity"
    CLOSED = "When no open position standing"

    @property
    def description(self):
        return self.value