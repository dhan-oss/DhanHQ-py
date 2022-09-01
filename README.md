# DhanHQ - v1.0


The official Python client for communicating with the [Dhan API](https://api.dhan.co)  

DhanHQ Rest API is used to automate investing and trading. Order execution in real time, Portfolio management, Check positions, holdings, funds and more with the simple HTTP API collection.


[Dhan](https://dhan.co) (c) 2022. Licensed under the Apache License 2.0

## Documentation

- [Python client documentation](https://github.com/dhan-oss/dhanhq)
- [Dhan HTTP API documentation](https://api.dhan.co)

## Features

* **Get Order list**  
Retrieve a list of all orders requested in a day with their last updated status.

* **Get Order by ID**  
Retrieve the details and status of an order from the orderbook placed during the day.

* **Modify Order**  
Modify pending order in orderbook. The variables that can be modified are price, quantity, order type & validity.

* **Cancel Order**  
Cancel a pending order in the orderbook using the order id of an order.

* **Place Order**  
Place new orders.

* **Get Order by Correlation ID**  
Retrieves the order status using a field called correlation id, Provided by API consumer during order placement.


* **Get Positions**  
Retrieve a list of all open positions for the day. This includes all F&O carryforward positions as well.

* **Get Holdings**  
Retrieve all holdings bought/sold in previous trading sessions. All T1 and delivered quantities can be fetched.

* **Intraday Daily Minute Charts**  
Retrieve OHLC & Volume of 1 minute candle for desired instrument for current day. This data available for all segments including futures & options.

* **Historical Minute Charts**  
Retrieve OHLC & Volume of daily candle for desired instrument. The data for any scrip is available back upto the date of its inception.

* **Get trade book**  
Retrieve a list of all trades executed in a day.

* **Get trade history**  
Retrieve the trade history Often during partial trades or Bracket/ Cover Orders, traders get confused in reading trade from tradebook. The response of this API will include all the trades generated for a particular order id.

* **Get fund limits**  
Get all information of your trading account like balance, margin utilised, collateral, etc.

## Quickstart

You can install the package via pip

```
pip install dhanhq
```



## Hands-on

```python
from dhanhq import dhanhq


dhan = dhanhq("client_id","access_token")

# Place an order
dhan.place_order(security_id= '1333' #hdfc bank
    exchange_seg= 'NSE_EQ'
    transaction_type= 'BUY'
    quantity=10
    order_type='MARKET'
    validity= 'DAY'
    product_type= 'INTRADAY'
    price=0
    trigger_price=0)
    


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

# Intraday daily minute charts
dhan.intraday_daily_minute_charts(security_id,exchange_segment,instrument_type)

# Historical Minute charts
dhan.historical_minute_charts(symbol,exchange_segment,instrument_type,expiry_code,from_date,to_date)

# Get trade book
dhan.get_trade_book(order_id)

# Get trade history
dhan.get_trade_history(from_date,to_date,page_number=0)

# Get fund limits
dhan.get_fund_limits()


```

Refer to the [Python client documentation](https://github.com/dhan-oss/dhanhq) for the complete list of supported methods.




## Changelog

[Check release notes](https://github.com/dhanhq/dhanhq/releases)