from dhanhq import dhanhq
import logging

logging.basicConfig(level=logging.DEBUG)

dhan = dhanhq(your_client_id, "your_access_token")

# Replace  your_client_id with Dhan Client ID.
# Replace "your_access_token" with your access token. Do remember it needs to be inside "".

# Place an order for Equity Cash
dhan.place_order(security_id='1333',            # HDFC Bank
    exchange_segment=dhan.NSE,
    transaction_type=dhan.BUY,
    quantity=10,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)
    
# Place an order for NSE Futures & Options
dhan.place_order(security_id='52175',           # Nifty PE
    exchange_segment=dhan.NSE_FNO,
    transaction_type=dhan.BUY,
    quantity=550,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)
    
# Place an order for Currency
dhan.place_order(security_id= '10093',          # USDINR
    exchange_segment= dhan.CUR,
    transaction_type= dhan.BUY,
    quantity=1,
    order_type = dhan.MARKET,
    validity= dhan.DAY,
    product_type= dhan.INTRA,
    price=0)

# Place an order for BSE Equity
dhan.place_order(security_id='500180',          # HDFC Bank
    exchange_segment=dhan.BSE,
    transaction_type=dhan.BUY,
    quantity=1,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0,)

# Place an order for BSE Futures & Options
dhan.place_order(security_id='1135553',         # Sensex PE
    exchange_segment=dhan.BSE_FNO,
    transaction_type=dhan.BUY,
    quantity=1,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0,)
    
# Place an order for MCX Commodity    
dhan.place_order(security_id= '114',            # Gold
    exchange_segment= dhan.MCX,
    transaction_type= dhan.BUY,
    quantity=1,
    order_type=dhan.MARKET,
    product_type= dhan.INTRA,
    price=0)
    
# Place Slice Order
dhan.place_slice_order(security_id='52175',     # Nifty PE
    exchange_segment=dhan.NSE_FNO,
    transaction_type=dhan.BUY,
    quantity=2000,              #Nifty freeze quantity is 1800
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)
   
# Place MTF Order
dhan.place_order(security_id='1333',            # HDFC Bank
    exchange_segment=dhan.NSE,
    transaction_type=dhan.BUY,
    quantity=100,
    order_type=dhan.MARKET,
    product_type=dhan.MTF,
    price=0)


# Fetch all orders
dhan.get_order_list()

# Get order by id
dhan.get_order_by_id(order_id)

# Modify order
dhan.modify_order(
    order_id= "13200000321",
    order_type= dhan.LIMIT,
    leg_name= "ENTRY_LEG", 
    quantity= 10,                   # Enter modified quantity or skip it
    price= 200,                     # Enter modified price or skip it
    trigger_price= 0, 
    disclosed_quantity= 0, 
    validity= dhan.DAY)

# Cancel order
dhan.cancel_order(order_id)

# Get order by correlation id
dhan.get_order_by_corelationID(correlationID)

# Get trade book
dhan.get_trade_book()

# Get trades of an order
dhan.get_trade_book(order_id)

# Get trade history
dhan.get_trade_history(from_date,to_date,page_number=0)
