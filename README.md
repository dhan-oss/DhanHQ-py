# DhanHQ-py : v2.0.2

[![PyPI](https://img.shields.io/pypi/v/dhanhq.svg)](https://pypi.org/project/dhanhq/)


The official Python client for communicating with the [Dhan API](https://api.dhan.co/v2/)  

DhanHQ-py Rest API is used to automate investing and trading. Execute orders in real time along with position management, live and historical data, tradebook and more with simple API collection.

Not just this, you also get real-time market data via DhanHQ Live Market Feed.


[Dhan](https://dhan.co) (c) 2024. Licensed under the [MIT License](https://github.com/dhan-oss/DhanHQ-py/blob/main/LICENSE)

### Documentation

- [DhanHQ Developer Kit](https://api.dhan.co/v2/)
- [DhanHQ API Documentation](https://dhanhq.co/docs/v2/)

## v2.1 - What's new

DhanHQ v2.1 is more modular and secure.

- The project is restructured to contemporary "best practices" in the python world. How does this affect you? Your imports would change like below:


  | Before This Version                                                    | After This Release                               |
  |------------------------------------------------------------------------|--------------------------------------------------|
  | from dhanhq import dhanhq | from dhanhq import dhanhq |
  | from dhanhq import marketfeed.DhanFeed | from dhanhq import DhanFeed |
  | from dhanhq import orderupdate.OrderSocket | from dhanhq import OrderSocket |

- The constants that were earlier part of modules `marketfeed` and `orderupdate` are now moved to its respective classes contained in the modules for better developer experience. 

  | Before This Version | After This Release |
  |---------------------|--------------------|
  | marketfeed.NSE      | DhanFeed.NSE       |
  | marketfeed.Ticker | DhanFeed.Ticker |

  Note: This improves developer experience to not knowing the entire package hierarchy and stay productive to know the interfaces he is working with. 


- Its SDK users, no longer have to repeat and spread the `client-id` and `access-token` around their code based in using our APIs. With this release, you defined it once for `DhanContext` and pass on this to different classes of the SDK instead of the raw credential strings, making your codebase much secure from data leaks and your coding a lot easier by defining DhanContext just once and use that context for other API classes. Quick glance of how affected code initialization is below:

  | Before This Version                                | After This Release                   |
  |----------------------------------------------------|--------------------------------------|
  | `dhanhq('client_id','access_token')`               | `dhanhq('dhan_context')`              |
  | `DhanFeed('client_id','access_token',instruments)` | `DhanFeed('dhan_context',instruments)` |
  | `OrderSocket('client_id','access_token')`          | `OrderSocket('dhan_context')`         |

  **Note:** The **_Hands-on API_** section is updated to reflect this change, for your convenience.

- Code coverage improvements with robust unit & integration tests for safe and speed delivery of features. Will strengthen even more in upcoming releases.

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
from dhanhq import DhanContext, dhanhq

dhan_context = DhanContext("client_id","access_token")
dhan = dhanhq(dhan_context)

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
    quantity= 10,
    price= 1900,
    trigger_Price= 1950
)
```

### Market Feed Usage
```python
from dhanhq import DhanContext, DhanFeed

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanContext("client_id","access_token")

# Structure for subscribing is (exchange_segment, "security_id", subscription_type)

instruments = [(DhanFeed.NSE, "1333", DhanFeed.Ticker),   # Ticker - Ticker Data
    (DhanFeed.NSE, "1333", DhanFeed.Quote),     # Quote - Quote Data
    (DhanFeed.NSE, "1333", DhanFeed.Full),      # Full - Full Packet
    (DhanFeed.NSE, "11915", DhanFeed.Ticker),
    (DhanFeed.NSE, "11915", DhanFeed.Full)]

version = "v2"          # Mention Version and set to latest version 'v2'

# In case subscription_type is left as blank, by default Ticker mode will be subscribed.

try:
    data = DhanFeed(dhan_context, instruments, version)
    while True:
        data.run_forever()
        response = data.get_data()
        print(response)

except Exception as e:
    print(e)

# Close Connection
data.disconnect()

# Subscribe instruments while connection is open
sub_instruments = [(DhanFeed.NSE, "14436", DhanFeed.Ticker)]

data.subscribe_symbols(sub_instruments)

# Unsubscribe instruments which are already active on connection
unsub_instruments = [(DhanFeed.NSE, "1333", 16)]

data.unsubscribe_symbols(unsub_instruments)
```

### Live Order Update Usage
```python
from dhanhq import DhanContext, OrderSocket
import time

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanContext("client_id","access_token")

def run_order_update():
    order_client = OrderSocket(dhan_context)
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
