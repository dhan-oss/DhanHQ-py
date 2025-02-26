import logging
from dhanhq.api import DhanCore, DhanConnection
from dhanhq.constants import ExchangeSegment, LegName, OrderType, ProductType, TransactionType, Validity

logging.basicConfig(level=logging.DEBUG)

dhan_context = DhanConnection("client_id", "access_token")
dhan = DhanCore(dhan_context)

# Replace  your_client_id with Dhan Client ID.
# Replace "your_access_token" with your access token. Do remember it needs to be inside "".

# Place an order for Equity Cash
dhan.orderEndpoint.place_order(security_id='1333',            # HDFC Bank
    exchange_segment=ExchangeSegment.NSE_EQ,
    transaction_type=TransactionType.BUY,
    quantity=10,
    order_type=OrderType.MARKET,
    product_type=ProductType.INTRADAY,
    price=0)

# Place an order for NSE Futures & Options
dhan.orderEndpoint.place_order(security_id='52175',           # Nifty PE
    exchange_segment=ExchangeSegment.NSE_FNO,
    transaction_type=TransactionType.BUY,
    quantity=550,
    order_type=OrderType.MARKET,
    product_type=ProductType.INTRADAY,
    price=0)

# Place an order for Currency
dhan.orderEndpoint.place_order(security_id= '10093',          # USDINR
    exchange_segment= ExchangeSegment.NSE_CURRENCY,
    transaction_type= TransactionType.BUY,
    quantity=1,
    order_type = OrderType.MARKET,
    validity= Validity.DAY,
    product_type= ProductType.INTRADAY,
    price=0)

# Place an order for BSE Equity
dhan.orderEndpoint.place_order(security_id='500180',          # HDFC Bank
    exchange_segment=ExchangeSegment.BSE_EQ,
    transaction_type=TransactionType.BUY,
    quantity=1,
    order_type=OrderType.MARKET,
    product_type=ProductType.INTRADAY,
    price=0,)

# Place an order for BSE Futures & Options
dhan.orderEndpoint.place_order(security_id='1135553',         # Sensex PE
    exchange_segment=ExchangeSegment.BSE_FNO,
    transaction_type=TransactionType.BUY,
    quantity=1,
    order_type=OrderType.MARKET,
    product_type=ProductType.INTRADAY,
    price=0,)

# Place an order for MCX Commodity
dhan.orderEndpoint.place_order(security_id= '114',            # Gold
    exchange_segment= ExchangeSegment.MCX_COMM,
    transaction_type= TransactionType.BUY,
    quantity=1,
    order_type=OrderType.MARKET,
    product_type= ProductType.INTRADAY,
    price=0)

# Place Slice Order
dhan.orderEndpoint.place_slice_order(security_id='52175',     # Nifty PE
    exchange_segment=ExchangeSegment.NSE_FNO,
    transaction_type=TransactionType.BUY,
    quantity=2000,              #Nifty freeze quantity is 1800
    order_type=OrderType.MARKET,
    product_type=ProductType.INTRADAY,
    price=0)

# Place MTF Order
dhan.orderEndpoint.place_order(security_id='1333',            # HDFC Bank
    exchange_segment=ExchangeSegment.NSE_EQ,
    transaction_type=TransactionType.BUY,
    quantity=100,
    order_type=OrderType.MARKET,
    product_type=ProductType.MTF,
    price=0)


# Fetch all orders
dhan.orderEndpoint.get_order_list()
order_id= "13200000321"

# Get order by id
dhan.orderEndpoint.get_order_by_id(order_id)

# Modify order
dhan.orderEndpoint.modify_order(
    order_id= "13200000321",
    order_type= OrderType.LIMIT,
    leg_name= LegName.ENTRY_LEG,
    quantity= 10,                   # Enter modified quantity or skip it
    price= 200,                     # Enter modified price or skip it
    trigger_price= 0,
    disclosed_quantity= 0,
    validity= Validity.DAY)

# Cancel order
dhan.orderEndpoint.cancel_order(order_id)

# Get order by correlation id
dhan.orderEndpoint.get_order_by_correlationID("correlationID")

# Get trade book
dhan.statementEndpoint.get_trade_book()

# Get trades of an order
dhan.statementEndpoint.get_trade_book(order_id)

# Get trade history
from_date = "2025-01-01"
to_date = "2025-01-31"
dhan.statementEndpoint.get_trade_history(from_date,to_date,page_number=0)
