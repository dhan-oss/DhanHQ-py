from enum import Enum

class LegName(Enum):
    ENTRY_LEG = "Entry Leg"
    STOP_LOSS_LEG = "Stop Loss Leg"
    TARGET_LEG = "Target Leg"
    NA = "Not Applicable"

    @property
    def description(self):
        return self.value
