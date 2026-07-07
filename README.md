# DhanHQ-py : v2.3.0-rc1 (Pre-release)

[![PyPI](https://img.shields.io/pypi/v/dhanhq.svg)](https://pypi.org/project/dhanhq/)

> ⚠️ **Pre-release / Release Candidate.** `v2.3.0rc1` is a release candidate for testing the new features below. It is not the latest stable release, so `pip install dhanhq` will not pick it up. Install it explicitly:
```bash
pip install --pre dhanhq==2.3.0rc1
```

The official Python client for communicating with the [Dhan API](https://api.dhan.co/v2/)  

DhanHQ-py Rest API is used to automate investing and trading. Execute orders in real time along with position management, live and historical data, tradebook and more with simple API collection.

Not just this, you also get real-time market data via DhanHQ Live Market Feed.


[Dhan](https://dhan.co) (c) 2026. Licensed under the [MIT License](https://github.com/dhan-oss/DhanHQ-py/blob/main/LICENSE)

### Documentation

- [DhanHQ Python Documentation](https://docs.dhanhq.co/api/v2/guides/sdks/python)
- [DhanHQ Developer Kit](https://api.dhan.co/v2/)
- [DhanHQ API Documentation](https://docs.dhanhq.co/api/v2/)

## v2.3.0-rc1 - What's new (Pre-release)
> This is a **release candidate**. APIs in this section are new and may change before the final `v2.3.0` release. Install with `pip install --pre dhanhq==2.3.0rc1`.

- **Conditional Orders** - place one or more orders automatically when a price or technical-indicator condition is met (Equities & Indices).
- **Global Stocks** - trade US stocks: orders, trades, holdings, fund limit, market status, order/charge estimate and margin. A separate Global Stocks instrument list is available too.
- **Global Stocks Live Feed** - real-time US stock Trade and OHLC packets over WebSocket via the new `GlobalStocksFeed`.
- **P&L based Exit** - auto square-off when cumulative profit or loss hits the configured absolute value thresholds (Trader's Control).
- **Multi-leg Margin Calculator** - compute combined margin for multiple orders with hedge benefits.

And a lot more is available directly on DhanHQ Python Library now.

---


## v2.2.0 - What's new
- You can now access the entire full market depth (200 Level) via DhanHQ APIs and part of the python library.
- Expired Options Data are now directly available on the library and you can fetch for all NSE & BSE instruments
- Super Orders - smart orders for managing risk and profits is now introduced with DhanHQ
- You can set, modify and change IP for your account, right from the python library - the code for the same is available under example.

And a lot more is available directly on DhanHQ Python Library now.

You can read about all other updates from DhanHQ V2 here: [DhanHQ Releases](https://docs.dhanhq.co/api/v2/guides/releases/).

---

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

* **Conditional Orders**  
Place one or more orders automatically when a price or technical-indicator condition is met, for Equities & Indices.

* **Global Stocks**  
Trade US stocks - place, modify and cancel orders, fetch trades, holdings, fund limit and market status, plus order/charge and margin estimates. A live feed for US stocks is available too.

* **P&L based Exit & Multi-leg Margin**  
Auto square-off on cumulative profit/loss thresholds and calculate combined margin for multiple orders with hedge benefits.

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
dhan.get_order_by_correlationID(correlationID)

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
dhan.convert_to_date_time(epoch_date)

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
dhan.edis_inquiry(isin='INE00IN01015')

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

# Place a Conditional Order (triggers orders when condition is met; Equities & Indices only)
dhan.place_conditional_order(
    condition={
        "comparisonType": "PRICE_WITH_VALUE",
        "exchangeSegment": dhan.NSE,
        "securityId": "1333",
        "operator": "GREATER_THAN",
        "comparingValue": 250,
        "frequency": "ONCE"                 # ONCE or ALWAYS
    },
    orders=[{
        "transactionType": dhan.BUY,
        "exchangeSegment": dhan.NSE,
        "productType": dhan.CNC,
        "orderType": dhan.LIMIT,
        "securityId": "1333",
        "quantity": 10,
        "validity": dhan.DAY,
        "price": "250.00"
    }]
)
dhan.get_conditional_orders()
dhan.cancel_conditional_order("12345")

# Global Stocks (US) - prices in USD
dhan.place_global_order(
    security_id="AAPL_SECURITY_ID",
    transaction_type=dhan.BUY,
    order_type=dhan.LIMIT,
    quantity=5,
    price=150.50
)
dhan.get_global_holdings()
dhan.get_global_fund_limit()
dhan.get_global_market_status()

# Fetch the Global Stocks (US) instrument list (distinct from the Indian list)
dhan.fetch_global_security_list()

# P&L based Exit (values are absolute amounts, not percentages)
dhan.set_pnl_exit(profit_value=1500, loss_value=500,
    product_type=["INTRADAY", "DELIVERY"], enable_kill_switch=True)
dhan.get_pnl_exit()
dhan.stop_pnl_exit()

# Multi-leg Margin Calculator
dhan.margin_calculator_multi(
    scrip_list=[
        {"securityId": "26009", "exchangeSegment": dhan.NSE_FNO, "transactionType": dhan.BUY,
         "quantity": 50, "productType": dhan.INTRA, "price": 45000.00},
        {"securityId": "26010", "exchangeSegment": dhan.NSE_FNO, "transactionType": dhan.SELL,
         "quantity": 50, "productType": dhan.INTRA, "price": 45500.00}
    ]
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
    data.run_forever()
    
    while True:
        response = data.get_data()
        print(response)

except Exception as e:
    print(e)
```

```
# Close Connection
data.close_connection()

# Subscribe instruments while connection is open
sub_instruments = [(MarketFeed.NSE, "14436", MarketFeed.Ticker)]

data.subscribe_symbols(sub_instruments)

# Unsubscribe instruments which are already active on connection
unsub_instruments = [(MarketFeed.NSE, "1333", 16)]

data.unsubscribe_symbols(unsub_instruments)
```

### Global Stocks Live Feed Usage
```python
from dhanhq import DhanContext, GlobalStocksFeed

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanContext("client_id","access_token")

# Structure for subscribing is (exchange_segment, "security_id", request_code)
# request_code is GlobalStocksFeed.SubscribeTrade (15) or GlobalStocksFeed.SubscribeOHLC (17).
# A 2-tuple defaults to the Trade feed.
instruments = [
    (GlobalStocksFeed.INX_EQ, "1234"),                                  # Trade
    (GlobalStocksFeed.INX_EQ, "5678", GlobalStocksFeed.SubscribeOHLC),  # OHLC
]

try:
    feed = GlobalStocksFeed(dhan_context, instruments, auth_type=GlobalStocksFeed.AUTH_SELF)
    feed.run_forever()

    while True:
        response = feed.get_data()
        print(response)

except Exception as e:
    print(e)
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
    response = FullDepth(dhan_context, instruments, depth_level)          #depth_level is non mandatory for 20 depth
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

