from enum import Enum

class AMOTime(Enum):
    PRE_OPEN = "AMO pumped at pre-market session"
    OPEN = "AMO pumped at market open"
    OPEN_30 = "AMO pumped 30 minutes after market open"
    OPEN_60 = "AMO pumped 60 minutes after market open"

    @property
    def description(self):
        return self.value