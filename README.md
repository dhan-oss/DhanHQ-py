# DhanHQ-py : v1.3

[![PyPI](https://img.shields.io/pypi/v/dhanhq.svg)](https://pypi.org/project/dhanhq/)


The official Python client for communicating with the [Dhan API](https://api.dhan.co)  

DhanHQ-py Rest API is used to automate investing and trading. Execute orders in real time along with position management, historical data, tradebook and more with simple API collection.

Not just this, you also get real-time market data via DhanHQ Live Market Feed.


[Dhan](https://dhan.co) (c) 2024. Licensed under the [MIT License](https://github.com/dhan-oss/DhanHQ-py/blob/main/LICENSE)

### Documentation

- [DhanHQ Developer Kit](https://api.dhan.co)
- [DhanHQ API Documentation](https://dhanhq.co/docs/v1/)

### v1.3 - What's New

Live Market Feed data is now available across exchanges and segments via DhanHQ
    
- Low latency websockets
- Unlimited instruments per socket
- Establish upto 5 sockets per user

With Market Feed, you can subscribe data in below formats:

- Ticker Data
- Quote Data
- Market Depth

## Features

* **Order Management**  
The order management APIs lets you place a new order, cancel or modify the pending order, retrieve the order status, trade status, order book & tradebook.

* **Live Market Feed**  
Get real-time market data to power your trading systems, with easy to implement functions and data across exchanges.

* **Portfolio**  
With this set of APIs, retrieve your holdings and positions in your portfolio.

* **Historical Data**  
Get historical candle data for the desired scrip across segments & exchange, both Intraday 1 minute OHLC and Daily OHLC.

* **Get fund limits**  
Get all information of your trading account like balance, margin utilised, collateral, etc.

* **eDIS Authorisation**  
To sell holding stocks, one needs to complete the CDSL eDIS flow, generate T-PIN & mark stock to complete the sell action.

## Quickstart

You can install the package via pip

```
pip install dhanhq
```



### Hands-on API

```python
from dhanhq import dhanhq

dhan = dhanhq("client_id","access_token")

# Place an order for Equity Cash
dhan.place_order(security_id='1333',   #hdfcbank
    exchange_segment=dhan.NSE,
    transaction_type=dhan.BUY,
    quantity=10,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)
    
# Place an order for NSE Futures & Options
dhan.place_order(security_id='52175',  #NiftyPE
    exchange_segment=dhan.NSE_FNO,
    transaction_type=dhan.BUY,
    quantity=550,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)
    
# Place an order for Currency
dhan.place_order(security_id= '10093',  #usdinr
    exchange_segment= dhan.CUR,
    transaction_type= dhan.BUY,
    quantity=1,
    order_type = dhan.MARKET,
    validity= dhan.DAY,
    product_type= dhan.INTRA,
    price=0)

# Place an order for BSE Equity
dhan.place_order(security_id='500180',   #hdfcbank
    exchange_segment=dhan.BSE,
    transaction_type=dhan.BUY,
    quantity=1,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0,)

# Place an order for BSE Futures & Options
dhan.place_order(security_id='1135553',   #SensexPE
    exchange_segment=dhan.BSE_FNO,
    transaction_type=dhan.BUY,
    quantity=1,
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0,)
    
# Place an order for MCX Commodity    
dhan.place_order(security_id= '114',    #gold
    exchange_segment= dhan.MCX,
    transaction_type= dhan.BUY,
    quantity=1,
    order_type=dhan.MARKET,
    product_type= dhan.INTRA,
    price=0)
    
# Place Slice Order
dhan.place_slice_order(security_id='52175',  #NiftyPE
    exchange_segment=dhan.NSE_FNO,
    transaction_type=dhan.BUY,
    quantity=2000,              #nifty freeze quantity is 1800
    order_type=dhan.MARKET,
    product_type=dhan.INTRA,
    price=0)
   
# Place MTF Order
dhan.place_order(security_id='1333',   #hdfcbank
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

# modify order
dhan.modify_order(order_id, order_type, leg_name, quantity, price, trigger_price, disclosed_quantity, validity)

# Cancel order
dhan.cancel_order(order_id)

# Get order by correlation id
dhan.get_order_by_corelationID(corelationID)

# Get positions
dhan.get_positions()

# Get holdings
dhan.get_holdings()

# Intraday Minute Data
dhan.intraday_minute_data(security_id,exchange_segment,instrument_type)

# Historical Daily Data
dhan.historical_daily_data(symbol,exchange_segment,instrument_type,expiry_code,from_date,to_date)

# Time Converter
dhan.convert_to_date_time(Julian Date)

# Get trade book
dhan.get_trade_book(order_id)

# Get trade history
dhan.get_trade_history(from_date,to_date,page_number=0)

# Get fund limits
dhan.get_fund_limits()

# Generate TPIN
dhan.generate_tpin()

# Enter TPIN in Form
dhan.open_browser_for_tpin(isin='INE00IN01015',
    qty=1,
    exchange='NSE')

# EDIS Status and Inquiry
dhan.edis_inquiry()
```

### Market Feed Usage
```python
from dhanhq import marketfeed

# Add your Dhan Client ID and Access Token
client_id = "Dhan Client ID"
access_token = "Access Token"

# Structure for subscribing is ("exchange_segment","security_id")

# Maximum 100 instruments can be subscribed, then use 'subscribe_symbols' function 

instruments = [(1, "1333"),(0,"13")]

# Type of data subscription
subscription_code = marketfeed.Ticker

# Ticker - Ticker Data
# Quote - Quote Data
# Depth - Market Depth


async def on_connect(instance):
    print("Connected to websocket")

async def on_message(instance, message):
    print("Received:", message)

print("Subscription code :"subscription_code)

feed = marketfeed.DhanFeed(client_id,
    access_token,
    instruments
    subscription_code
    on_connect=on_connect,
    on_message=on_message)

feed.run_forever()
```


## Changelog

[Check release notes](https://github.com/dhan-oss/DhanHQ-py/releases)
