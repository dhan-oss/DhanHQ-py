from dhanhq import DhanContext, dhanhq

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)
dhan = dhanhq(dhan_context)

# 2. Place Forever Order (Single)
print("\nPlacing Forever Order (Single)...")
try:
    response = dhan.place_forever(
        security_id="1333",       # HDFC Bank
        exchange_segment=dhan.NSE,
        transaction_type=dhan.BUY,
        order_type=dhan.LIMIT,
        product_type=dhan.CNC,
        quantity=10,
        price=1500,
        trigger_Price=1510
    )
    print(response)
except Exception as e:
    print(f"Error placing forever order: {e}")

# 3. Place Forever Order (OCO)
print("\nPlacing Forever Order (OCO)...")
try:
    response = dhan.place_forever(
        security_id="1333",
        exchange_segment=dhan.NSE,
        transaction_type=dhan.SELL,
        order_type=dhan.LIMIT,
        product_type=dhan.CNC,
        quantity=10,
        price=1600,
        trigger_Price=1610,
        order_flag="OCO",
        price1=1400,          # Stop Loss Price
        trigger_Price1=1410   # Stop Loss Trigger Price
    )
    print(response)
except Exception as e:
    print(f"Error placing OCO forever order: {e}")
