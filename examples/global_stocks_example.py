from dhanhq import DhanContext, dhanhq

# Replace with your Dhan Client ID and access token
dhan_context = DhanContext("client_id", "access_token")
dhan = dhanhq(dhan_context)

# Global Stocks lets you trade US stocks. The instrument list is distinct from the
# Indian one - fetch it with the security_id values used below:
#   df = dhan.fetch_global_security_list()

# Place a LIMIT buy order for a US stock (prices are in USD)
dhan.place_global_order(
    security_id="AAPL_SECURITY_ID",
    transaction_type=dhan.BUY,
    order_type=dhan.LIMIT,
    quantity=5,
    price=150.50,
)

# Place a market order
dhan.place_global_order(
    security_id="AAPL_SECURITY_ID",
    transaction_type=dhan.BUY,
    order_type=dhan.MARKET,
    quantity=1,
    price=0,
)

# Fetch the US stock order book
dhan.get_global_order_list()

# Fetch a specific order
dhan.get_global_order_by_id("112111182198")

# Modify a pending order
dhan.modify_global_order(
    order_id="112111182198",
    order_type=dhan.LIMIT,
    transaction_type=dhan.BUY,
    security_id="AAPL_SECURITY_ID",
    quantity=3,
    price=149.00,
)

# Cancel a pending order
dhan.cancel_global_order("112111182198")

# Trades, holdings and fund limit
dhan.get_global_trades()
dhan.get_global_trades_by_security("AAPL_SECURITY_ID")
dhan.get_global_holdings()
dhan.get_global_fund_limit()

# Estimate charges and margin before placing an order
dhan.global_trans_estimate("AAPL_SECURITY_ID", "150.50", "5", dhan.BUY)
dhan.global_margin_calculator("AAPL_SECURITY_ID", "150.50", "5", dhan.BUY)

# Check whether the US market is open
dhan.get_global_market_status()

# Fetch the Global Stocks (US) instrument list CSV
dhan.fetch_global_security_list()
