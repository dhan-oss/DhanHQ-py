from dhanhq import DhanContext, dhanhq

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)
dhan = dhanhq(dhan_context)

# 2. Place Super Order
# Super Orders allow placing orders with Stop Loss and Target Price
print("\nPlacing Super Order...")
try:
    response = dhan.place_super_order(
        security_id="1333",          # HDFC Bank
        exchange_segment=dhan.NSE,
        transaction_type=dhan.BUY,
        quantity=10,
        order_type=dhan.MARKET,
        product_type=dhan.INTRADAY,
        price=0,
        target_price=1600,           # Target Price
        stop_loss_price=1450         # Stop Loss Price
    )
    print(response)
except Exception as e:
    print(f"Error placing super order: {e}")
