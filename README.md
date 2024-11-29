# DhanHQ-py : v2.0.2

[![PyPI](https://img.shields.io/pypi/v/dhanhq.svg)](https://pypi.org/project/dhanhq/)


The official Python client for communicating with the [Dhan API](https://api.dhan.co/v2/)  

DhanHQ-py Rest API is used to automate investing and trading. Execute orders in real time along with position management, live and historical data, tradebook and more with simple API collection.

Not just this, you also get real-time market data via DhanHQ Live Market Feed.


[Dhan](https://dhan.co) (c) 2024. Licensed under the [MIT License](https://github.com/dhan-oss/DhanHQ-py/blob/main/LICENSE)

### Documentation

- [DhanHQ Developer Kit](https://api.dhan.co/v2/)
- [DhanHQ API Documentation](https://dhanhq.co/docs/v2/)


## v2.0 - What's New

DhanHQ v2 extends execution capability with live order updates, market quotes and forever orders on superfast APIs. Some of the key highlights from this version are:
    
- Fetch LTP, Quote (with OI) and Market Depth data directly on API, for upto 1000 instruments at once with Market Quote API.

- Option Chain API which gives OI, greeks, volume, top bid/ask and price data of all strikes of a particular underlying.

- Place, modify and manage your Forever Orders, including single and OCO orders to manage risk and trade efficiently with Forever Order API.

- Order Updates are sent in real time via websockets, which will update order status of all your orders placed via any platform - `order_update`.

- Intraday Minute Data now provides OHLC with Volume data for last 5 trading days across timeframes such as 1 min, 5 min, 15 min, 25 min and 60 min - `intraday_minute_data`.

- Full Packet in Live Market Feed (`marketfeed`).

- Margin Calculator (`margin_calculator`) and Kill Switch (`kill_switch`) APIs.

### Breaking Changes

- Replaced `intraday_daily_minute_data` and `historical_minute_charts` as functions from v1.2.4

- `quantity` field needs to be placed order quantity instead of pending order quantity in Order Modification

- EPOCH time instead of Julian time in Historical Data API, and same changed for `convert_to_date_time` function

- `historical_daily_data` takes `security_id` as argument instead of `symbol`

- Nomenclature changes in `get_order_by_corelationID` to `get_order_by_correlationID`.

You can read about all other updates from DhanHQ V2 here: [DhanHQ Releases](https://dhanhq.co/docs/v2/releases/).


## Features

* **Order Management**  
The order management APIs lets you place a new order, cancel or modify the pending order, retrieve the order status, trade status, order book & tradebook.

* **Live Market Feed**  
Get real-time market data to power your trading systems, with easy to implement functions and data across exchanges.

* **Market Quote**  
REST APIs based market quotes which given you snapshot of ticker mode, quote mode or full mode.

* **Option Chain**  
Single function which gives entire Option Chain across exchanges and segments, giving OI, greeks, volume, top bid/ask and price data.

* **Forever Order**  
Place, modify or delete Forever Orders, whether single or OCO to better manage your swing trades.

* **Portfolio Management**  
With this set of APIs, retrieve your holdings and positions in your portfolio as well as manage them.

* **Historical Data**  
Get historical candle data for the desired scrip across segments & exchange, both multiple minute timeframe OHLC and Daily OHLC.

* **Fund Details**  
Get all information of your trading account like balance, margin utilised, collateral, etc as well margin required for any order.

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
  
# Fetch all orders
dhan.get_order_list()

# Get order by id
dhan.get_order_by_id(order_id)

# Modify order
dhan.modify_order(order_id, order_type, leg_name, quantity, price, trigger_price, disclosed_quantity, validity)

# Cancel order
dhan.cancel_order(order_id)

# Get order by correlation id
dhan.get_order_by_corelationID(corelationID)

# Get Instrument List
dhan.fetch_security_list("compact")

# Get positions
dhan.get_positions()

# Get holdings
dhan.get_holdings()

# Intraday Minute Data
dhan.intraday_minute_data(security_id,exchange_segment,instrument_type)

# Historical Daily Data
dhan.historical_daily_data(security_id,exchange_segment,instrument_type,expiry_code,from_date,to_date)

# Time Converter
dhan.convert_to_date_time(EPOCH Date)

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

# Expiry List of Underlying
dhan.expiry_list(
    under_security_id=13,                       # Nifty
    under_exchange_segment="IDX_I"
)

# Option Chain
dhan.option_chain(
    under_security_id=13,                       # Nifty
    under_exchange_segment="IDX_I",
    expiry="2024-10-31"
)

# Market Quote Data                     # LTP - ticker_data, OHLC - ohlc_data, Full Packet - quote_data
dhan.ohlc_data(
    securities = {"NSE_EQ":[1333]}
)

# Place Forever Order (SINGLE)
dhan.place_forever(
    security_id="1333",
    exchange_segment= dhan.NSE,
    transaction_type= dhan.BUY,
    product_type=dhan.CNC,
    product_type= dhan.LIMIT,
    quantity= 10,
    price= 1900,
    trigger_Price= 1950
)
```

### Market Feed Usage
```python
from dhanhq import marketfeed

# Add your Dhan Client ID and Access Token
client_id = "Dhan Client ID"
access_token = "Access Token"

# Structure for subscribing is (exchange_segment, "security_id", subscription_type)

instruments = [(marketfeed.NSE, "1333", marketfeed.Ticker),   # Ticker - Ticker Data
    (marketfeed.NSE, "1333", marketfeed.Quote),     # Quote - Quote Data
    (marketfeed.NSE, "1333", marketfeed.Full),      # Full - Full Packet
    (marketfeed.NSE, "11915", marketfeed.Ticker),
    (marketfeed.NSE, "11915", marketfeed.Full)]

version = "v2"          # Mention Version and set to latest version 'v2'

# In case subscription_type is left as blank, by default Ticker mode will be subscribed.

try:
    data = marketfeed.DhanFeed(client_id, access_token, instruments, version)
    while True:
        data.run_forever()
        response = data.get_data()
        print(response)

except Exception as e:
    print(e)

# Close Connection
data.disconnect()

# Subscribe instruments while connection is open
sub_instruments = [(marketfeed.NSE, "14436", marketfeed.Ticker)]

data.subscribe_symbols(sub_instruments)

# Unsubscribe instruments which are already active on connection
unsub_instruments = [(marketfeed.NSE, "1333", 16)]

data.unsubscribe_symbols(unsub_instruments)
```

### Live Order Update Usage
```python
from dhanhq import orderupdate
import time

# Add your Dhan Client ID and Access Token
client_id = "Dhan Client ID"
access_token = "Access Token"

def run_order_update():
    order_client = orderupdate.OrderSocket(client_id, access_token)
    while True:
        try:
            order_client.connect_to_dhan_websocket_sync()
        except Exception as e:
            print(f"Error connecting to Dhan WebSocket: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

run_order_update()
```

## Changelog

[Check release notes](https://github.com/dhan-oss/DhanHQ-py/releases)
