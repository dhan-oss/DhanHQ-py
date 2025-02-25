from enum import Enum

class OrderFlag(Enum):
    SINGLE = "Single Good Till Triggered (GTT) Order"
    OCO = "One Cancels the Other GTT Order"

    @property
    def description(self):
        return self.value
