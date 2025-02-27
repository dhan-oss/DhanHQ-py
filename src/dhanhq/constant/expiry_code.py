from enum import Enum

class ExpiryCode(Enum):
    CURRENT_OR_NEAR_EXPIRY = 0
    NEXT_EXPIRY = 1
    FAR_EXPIRY = 2