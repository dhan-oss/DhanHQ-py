from enum import Enum

class OrderStatus(Enum):
    TRANSIT = "Did not reach the exchange server "
    PENDING = "Reached at exchange end, awaiting execution"
    REJECTED = "Rejected at exchange/broker’s end"
    CANCELLED = "Cancelled by user"
    PART_TRADED = "Partially Executed"
    TRADED = "Executed"
    EXPIRED = "Validity of order_req is expired"