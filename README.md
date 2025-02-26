from dhanhq.constants.exchange_segment import ExchangeSegmentfrom dhanhq.constants.exchange_segment import ExchangeSegment

# DhanHQ-py : v3.0.0

[![PyPI](https://img.shields.io/pypi/v/dhanhq.svg)](https://pypi.org/project/dhanhq/)


The official Python client for communicating with the [Dhan API](https://api.dhan.co/v2/)  

DhanHQ-py Rest API is used to automate investing and trading. Execute orders in real time along with position management, live and historical data, tradebook and more with simple API collection.

Not just this, you also get real-time market data via DhanHQ Live Market Feed.


[Dhan](https://dhan.co) (c) 2024. Licensed under the [MIT License](https://github.com/dhan-oss/DhanHQ-py/blob/main/LICENSE)

### Documentation

- [DhanHQ Developer Kit](https://api.dhan.co/v2/)
- [DhanHQ API Documentation](https://dhanhq.co/docs/v2/)
- [DhanHQ Java SDK](https://github.com/karthiks/DhanHQ-java)

> Vision: SDK APIs irrespective of the language share common experience as much as possible and that the SDK APIs mimic the API Doc, so that the later is the single source of truth!

## v3.0.0

> This version's API is completely new from its earlier version that has come this far with incessant refactoring of the legacy code that was buggy (see Github issues of the repository) and had no test coverage. 

> Websockets are moved under `api.stream` package and the REST API endpoints are put under `api.ondemand` package. `DhanConnection` and `DhanCore` being the starting points for API interaction, are put under `api`. This SDK's API only gets better with your love, so start using it today in your algorithmic trading!

- Renamed `dhanhq` class to `DhanCore`
- Added Type-hints for static and dynamic type-checking of code and better end-user experience of SDK
- Extracted and grouped constants under varied classes/enums to avoid bugs
- API akin to Java SDK, to have unified API experience irrespective of language version SDK used to access Dhan APIs
- The code will become more object-oriented akin to its Java counterpart and as end-user developer you wouldn't miss the goodness of the language and the richness of the domain.

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
from dhanhq.api import DhanConnection, DhanCore
from dhanhq.constants import ExchangeSegment

dhan_context = DhanConnection("client_id", "access_token")
dhan = DhanCore(dhan_context)

# Place an order for Equity Cash
dhan.orderEndpoint.place_order(security_id='1333',  # HDFC Bank
                 exchange_segment=ExchangeSegment.NSE_EQ,
                 transaction_type=dhan.BUY,
                 quantity=10,
                 order_type=dhan.MARKET,
                 product_type=dhan.INTRA,
                 price=0)

# Place an order for NSE Futures & Options
dhan.orderEndpoint.place_order(security_id='52175',  # Nifty PE
                 exchange_segment=ExchangeSegment.NSE_FNO,
                 transaction_type=dhan.BUY,
                 quantity=550,
                 order_type=dhan.MARKET,
                 product_type=dhan.INTRA,
                 price=0)

# Fetch all orders
dhan.orderEndpoint.get_order_list()

# Get order by id
dhan.orderEndpoint.get_order_by_id(order_id)

# Modify order
dhan.orderEndpoint.modify_order(order_id, order_type, leg_name, quantity, price, trigger_price, disclosed_quantity, validity)

# Cancel order
dhan.orderEndpoint.cancel_order(order_id)

# Get order by correlation id
dhan.orderEndpoint.get_order_by_corelationID(corelationID)

# Get Instrument List
dhan.securityEndpoint.fetch_security_list("compact")

# Get positions
dhan.portfolioEndpoint.get_positions()

# Get holdings
dhan.portfolioEndpoint.get_holdings()

# Intraday Minute Data
dhan.orderEndpoint.intraday_minute_data(security_id, exchange_segment, instrument_type)

# Historical Daily Data
dhan.historicalDataEndpoint.historical_daily_data(security_id, exchange_segment, instrument_type, expiry_code, from_date, to_date)

# Time Converter
dhan.convert_to_date_time(EPOCHDate)

# Get trade book
dhan.statementEndpoint.get_trade_book(order_id)

# Get trade history
dhan.statementEndpoint.get_trade_history(from_date, to_date, page_number=0)

# Get fund limits
dhan.fundsEndpoint.get_fund_limits()

# Generate TPIN
dhan.securityEndpoint.generate_tpin()

# Enter TPIN in Form
dhan.securityEndpoint.open_browser_for_tpin(isin='INE00IN01015',
                           qty=1,
                           exchange='NSE')

# EDIS Status and Inquiry
dhan.securityEndpoint.edis_inquiry()

# Expiry List of Underlying
dhan.optionChainEndpoint.expiry_list(
  under_security_id=13,  # Nifty
  under_exchange_segment="IDX_I"
)

# Option Chain
dhan.optionChainEndpoint.option_chain(
  under_security_id=13,  # Nifty
  under_exchange_segment="IDX_I",
  expiry="2024-10-31"
)

# Market Quote Data                     # LTP - ticker_data, OHLC - ohlc_data, Full Packet - quote_data
dhan.marketFeedEndpoint.ohlc_data(
  securities={"NSE_EQ": [1333]}
)

# Place Forever Order (SINGLE)
dhan.foreverOrderEndpoint.place_forever(
  security_id="1333",
  exchange_segment=ExchangeSegment.NSE,
  transaction_type=dhan.BUY,
  product_type=dhan.CNC,
  quantity=10,
  price=1900,
  trigger_Price=1950
)
```

### Market Feed Usage

```python
from dhanhq.api import DhanConnection 
from dhanhq.api.stream import LiveMarketFeed

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanConnection("client_id", "access_token")

# Structure for subscribing is (exchange_segment, "security_id", subscription_type)

instruments = [(LiveMarketFeed.NSE, "1333", LiveMarketFeed.Ticker),  # Ticker - Ticker Data
               (LiveMarketFeed.NSE, "1333", LiveMarketFeed.Quote),  # Quote - Quote Data
               (LiveMarketFeed.NSE, "1333", LiveMarketFeed.Full),  # Full - Full Packet
               (LiveMarketFeed.NSE, "11915", LiveMarketFeed.Ticker),
               (LiveMarketFeed.NSE, "11915", LiveMarketFeed.Full)]

version = "v2"  # Mention Version and set to latest version 'v2'

# In case subscription_type is left as blank, by default Ticker mode will be subscribed.

try:
  data = LiveMarketFeed(dhan_context, instruments, version)
  while True:
    data.run_forever()
    response = data.get_data()
    print(response)

except Exception as e:
  print(e)

# Close Connection
data.disconnect()

# Subscribe instruments while connection is open
sub_instruments = [(LiveMarketFeed.NSE, "14436", LiveMarketFeed.Ticker)]

data.subscribe_symbols(sub_instruments)

# Unsubscribe instruments which are already active on connection
unsub_instruments = [(LiveMarketFeed.NSE, "1333", 16)]

data.unsubscribe_symbols(unsub_instruments)
```

### Live Order Update Usage

```python
from dhanhq.api import DhanConnection 
from dhanhq.api.stream import OrderSocket
import time

# Define and use your dhan_context if you haven't already done so like below:
dhan_context = DhanConnection("client_id", "access_token")


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
