from enum import Enum

class KillSwitchStatus(Enum):
    ACTIVATE = "Activate"
    DEACTIVATE = "Deactivate"

    @property
    def description(self):
        return self.value
