# DhanHQ-py : v2.2.0 [Pre-release]

[![PyPI](https://img.shields.io/pypi/v/dhanhq.svg)](https://pypi.org/project/dhanhq/)

> **Note: v2.2.0 is currently in pre-release.**
> With the release of v2.2.0, there are breaking changes of v2.1.0. You can install pre-release version by using the below code:
```bash
pip install --pre dhanhq
```


The official Python client for communicating with the [Dhan API](https://api.dhan.co/v2/)  

DhanHQ-py Rest API is used to automate investing and trading. Execute orders in real time along with position management, live and historical data, tradebook and more with simple API collection.

Not just this, you also get real-time market data via DhanHQ Live Market Feed.


[Dhan](https://dhan.co) (c) 2025. Licensed under the [MIT License](https://github.com/dhan-oss/DhanHQ-py/blob/main/LICENSE)

### Documentation

- [DhanHQ Python Documentation](https://dhanhq.co/docs/DhanHQ-py/)
- [DhanHQ Developer Kit](https://api.dhan.co/v2/)
- [DhanHQ API Documentation](https://dhanhq.co/docs/v2/)

## v2.2.0 - What's new
- You can now access the entire full market depth (200 Level) via DhanHQ APIs and part of the python library.
- Expired Options Data are now directly available on the library and you can fetch for all NSE & BSE instruments
- Super Orders - smart orders for managing risk and profits is now introduced with DhanHQ
- You can set, modify and change IP for your account, right from the python library - the code for the same is available under example.

And a lot more is available directly on DhanHQ Python Library now.

---


## v2.1.0 - What's new

- 20 level market depth is now available on DhanHQ APIs and part of the python library.

DhanHQ v2.1.0 is more modular and secure.

- The project is restructured to contemporary "best practices" in the python world. How does this affect you? Your imports would change like below:


  | Before This Version                                                    | After This Release                               |
  |------------------------------------------------------------------------|--------------------------------------------------|
  | from dhanhq import dhanhq | from dhanhq import dhanhq |
  | from dhanhq import marketfeed.MarketFeed | from dhanhq import MarketFeed |
  | from dhanhq import orderupdate.OrderUpdate | from dhanhq import OrderUpdate |

- The constants that were earlier part of modules `marketfeed` and `orderupdate` are now moved to its respective classes contained in the modules for better developer experience. 

  | Before This Version | After This Release |
  |---------------------|--------------------|
  | marketfeed.NSE      | MarketFeed.NSE       |
  | marketfeed.Ticker | MarketFeed.Ticker |

  Note: This improves developer experience to not knowing the entire package hierarchy and stay productive to know the interfaces he is working with. 


- You no longer have to repeat and spread the `client-id` and `access-token` around their code based in using our APIs. With this release, you defined it once for `DhanContext` and pass on this to different classes of the SDK instead of the raw credential strings, making your codebase much secure from data leaks and your coding a lot easier by defining DhanContext just once and use that context for other API classes. Quick glance of how affected code initialization is below:

  | Before This Version                                | After This Release                   |
  |----------------------------------------------------|--------------------------------------|
  | `dhanhq('client_id','access_token')`               | `dhanhq('dhan_context')`              |
  | `MarketFeed('client_id','access_token',instruments)` | `MarketFeed('dhan_context',instruments)` |
  | `OrderUpdate('client_id','access_token')`          | `OrderUpdate('dhan_context')`         |

  **Note:** The **_Hands-on API_** section is updated to reflect this change, for your convenience.

- Code coverage improvements with robust unit & integration tests for safe and speed delivery of features. Will strengthen even more in upcoming releases.

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



### Authentication

You can now generate access tokens using the `DhanLogin` class.

#### Method 1: OAuth Flow
```python
from dhanhq import DhanLogin

dhan_login = DhanLogin("YOUR_CLIENT_ID")
app_id = "YOUR_APP_ID"
app_secret = "YOUR_APP_SECRET"

# Step 1: Generate Consent and Open Browser for Login
consent_id = dhan_login.generate_login_session(app_id, app_secret)

# Step 2: Consume Token ID (After user logs in and gets Token ID from redirect URL)
token_id = "TOKEN_ID_FROM_REDIRECT_URL"
access_token = dhan_login.consume_token_id(token_id, app_id, app_secret)
print(access_token)
```

#### Method 2: PIN & TOTP Flow
```python
from dhanhq import DhanLogin

dhan_login = DhanLogin("YOUR_CLIENT_ID")
pin = "YOUR_PIN"
totp = "YOUR_TOTP"

access_token_data = dhan_login.generate_token(pin, totp)
print(access_token_data)
```

#### Renew Token
``` python
dhan_login.renew_token(access_token)
```

#### User Profile
``` python
# Check validity of access token and account setup
user_info = dhan_login.user_profile(access_token)
print(user_info)
```

### IP Management
You can manage your Static IP (whitelisting) using `set_ip`, `modify_ip`, and `get_ip`.
```python
# Set Primary IP
response = dhan_login.set_ip(access_token, "10.200.10.10", "PRIMARY")
print(response)
# Modify Primary IP
response = dhan_login.modify_ip(access_token, "10.200.10.11", "PRIMARY")
print(response)
# Get Configured IPs
ip_list = dhan_login.get_ip(access_token)
print(ip_list)
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
dhan.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date)

# Historical Daily Data
dhan.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date)

# Expired Options Data
dhan.expired_options_data(
    security_id=13,
    exchange_segment="NSE_FNO",
    instrument_type="INDEX",
    expiry_flag="MONTH",
    expiry_code=1,
    strike="ATM",
    drv_option_type="CALL",
    required_data=["open", "high", "low", "close", "volume"],
    from_date="2023-01-01",
    to_date="2023-01-31"
)

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
    order_type=dhan.LIMIT,
    product_type=dhan.CNC,
    quantity= 10,
    price= 1900,
    trigger_Price= 1950
)
```

### Market Feed Usage
```python
from dhanhq import DhanContext, MarketFeed

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanContext("client_id","access_token")

# Structure for subscribing is (exchange_segment, "security_id", subscription_type)

instruments = [(MarketFeed.NSE, "1333", MarketFeed.Ticker),   # Ticker - Ticker Data
    (MarketFeed.NSE, "1333", MarketFeed.Quote),     # Quote - Quote Data
    (MarketFeed.NSE, "1333", MarketFeed.Full),      # Full - Full Packet
    (MarketFeed.NSE, "11915", MarketFeed.Ticker),
    (MarketFeed.NSE, "11915", MarketFeed.Full)]

version = "v2"          # Mention Version and set to latest version 'v2'

# In case subscription_type is left as blank, by default Ticker mode will be subscribed.

try:
    data = MarketFeed(dhan_context, instruments, version)
    while True:
        data.run_forever()
        response = data.get_data()
        print(response)

except Exception as e:
    print(e)
```

```
# Close Connection
data.disconnect()

# Subscribe instruments while connection is open
sub_instruments = [(MarketFeed.NSE, "14436", MarketFeed.Ticker)]

data.subscribe_symbols(sub_instruments)

# Unsubscribe instruments which are already active on connection
unsub_instruments = [(MarketFeed.NSE, "1333", 16)]

data.unsubscribe_symbols(unsub_instruments)
```

### Live Order Update Usage
```python
from dhanhq import DhanContext, OrderUpdate
import time

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanContext("client_id","access_token")

def on_order_update(order_data: dict):
    """Optional callback function to process order data"""
    print(order_data["Data"])

def run_order_update():
    order_client = OrderUpdate(dhan_context)

    # Optional: Attach a callback function to receive and process order data.
    order_client.on_update = on_order_update

    while True:
        try:
            order_client.connect_to_dhan_websocket_sync()
        except Exception as e:
            print(f"Error connecting to Dhan WebSocket: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

run_order_update()
```

### Full Market Depth
```python
from dhanhq import DhanContext, FullDepth

dhan_context = DhanContext(client_id, access_token)

instruments = [(1, "1333")]                     #[(1, "1333"),(2,"")] for 20 depth, upto 50 instruments
depth_level = 200                               # 20 or 200, default 20 in case this is not passed

try:
    response = fulldepth.FullDepth(dhan_context, instruments, depth_level)          #depth_level is non mandatory for 20 depth
    response.run_forever()
    
    while True:
        response.get_data()
        
        if response.on_close:
            print("Server disconnection detected. Kindly try again.")
            break

except Exception as e:
    print(e)

```

## Changelog

[Check release notes](https://github.com/dhan-oss/DhanHQ-py/releases)

