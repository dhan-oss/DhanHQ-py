from dhanhq import DhanContext, dhanhq

# Replace with your Dhan Client ID and access token
dhan_context = DhanContext("client_id", "access_token")
dhan = dhanhq(dhan_context)

# Conditional Orders place one or more orders automatically when a price or
# technical-indicator condition is met. Supported only for Equities and Indices.

# Place a conditional order: when HDFC Bank LTP crosses above 250, buy 10 shares.
condition = {
    "comparisonType": "PRICE_WITH_VALUE",
    "exchangeSegment": dhan.NSE,            # NSE_EQ
    "securityId": "1333",                   # HDFC Bank
    "operator": "GREATER_THAN",
    "comparingValue": 250,
    "frequency": "ONCE",                    # ONCE or ALWAYS
}
orders = [{
    "transactionType": dhan.BUY,
    "exchangeSegment": dhan.NSE,
    "productType": dhan.CNC,
    "orderType": dhan.LIMIT,
    "securityId": "1333",
    "quantity": 10,
    "validity": dhan.DAY,
    "price": "250.00",
}]
dhan.place_conditional_order(condition, orders)

# Indicator based condition: trigger when 14-period RSI crosses above 70
indicator_condition = {
    "comparisonType": "TECHNICAL_WITH_VALUE",
    "exchangeSegment": dhan.NSE,
    "securityId": "1333",
    "indicatorName": "RSI_14",              # passed as a plain string
    "timeFrame": "FIFTEEN_MIN",
    "operator": "CROSSING_UP",
    "comparingValue": 70,
    "frequency": "ONCE",
}
dhan.place_conditional_order(indicator_condition, orders)

# Fetch all conditional orders
dhan.get_conditional_orders()

# Fetch a specific conditional order
dhan.get_conditional_order("12345")

# Modify a conditional order's condition (and optionally its orders)
condition["comparingValue"] = 260
dhan.modify_conditional_order("12345", condition, orders)

# Cancel a conditional order
dhan.cancel_conditional_order("12345")

# Multi Order places several orders in one request, directly and without any condition.
# Up to 15 orders per request, placed in the sequence given.
multi_orders = [
    {
        "sequence": "1",                    # required, starts at 1
        "correlationId": "my-batch-1",      # optional, up to 30 characters
        "transactionType": dhan.BUY,
        "exchangeSegment": dhan.NSE,        # NSE_EQ
        "productType": dhan.CNC,
        "orderType": dhan.LIMIT,
        "validity": dhan.DAY,
        "securityId": "1333",               # HDFC Bank
        "quantity": 10,
        "price": 250.00,
    },
    {
        "sequence": "2",
        "transactionType": dhan.SELL,
        "exchangeSegment": dhan.NSE,
        "productType": dhan.INTRA,          # INTRADAY
        "orderType": dhan.MARKET,
        "validity": dhan.DAY,
        "securityId": "11536",              # TCS
        "quantity": 5,
    },
]
# Each entry in the response holds orderId, sequence and orderStatus.
dhan.place_multi_order(multi_orders)
