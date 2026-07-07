from dhanhq import DhanContext, dhanhq

# Replace with your Dhan Client ID and access token
dhan_context = DhanContext("client_id", "access_token")
dhan = dhanhq(dhan_context)

# ----- P&L based exit (Trader's Control) -----
# Auto square-off when cumulative P&L hits the given thresholds.
# Note: profit_value and loss_value are absolute value amounts (in rupees), NOT percentages.
dhan.set_pnl_exit(
    profit_value=1500,                       # book profit at +1500
    loss_value=500,                          # stop loss at -500
    product_type=["INTRADAY", "DELIVERY"],
    enable_kill_switch=True,
)

# Fetch the active P&L exit configuration
dhan.get_pnl_exit()

# Disable the P&L exit configuration
dhan.stop_pnl_exit()

# ----- Multi-leg margin calculator (Funds) -----
# Calculate combined margin for multiple orders, with hedge benefits.
scrip_list = [
    {
        "securityId": "26009",
        "exchangeSegment": dhan.NSE_FNO,
        "transactionType": dhan.BUY,
        "quantity": 50,
        "productType": dhan.INTRA,
        "price": 45000.00,
    },
    {
        "securityId": "26010",
        "exchangeSegment": dhan.NSE_FNO,
        "transactionType": dhan.SELL,
        "quantity": 50,
        "productType": dhan.INTRA,
        "price": 45500.00,
    },
]
dhan.margin_calculator_multi(scrip_list, include_position=False, include_order=False)
