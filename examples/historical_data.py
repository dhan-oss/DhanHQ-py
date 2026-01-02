from dhanhq import DhanContext, dhanhq

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)
dhan = dhanhq(dhan_context)

# 2. Fetch Daily Historical Data
print("\nFetching Daily Historical Data...")
try:
    daily_data = dhan.historical_daily_data(
        security_id="1333",          # HDFC Bank
        exchange_segment=dhan.NSE,
        instrument_type="EQUITY",
        from_date="2023-01-01",
        to_date="2023-01-31"
    )
    print(daily_data)
except Exception as e:
    print(f"Error fetching daily data: {e}")

# 3. Fetch Intraday Minute Data
print("\nFetching Intraday Minute Data...")
try:
    intraday_data = dhan.intraday_minute_data(
        security_id="1333",
        exchange_segment=dhan.NSE,
        instrument_type="EQUITY",
        from_date="2023-01-30",
        to_date="2023-01-31"
    )
    print(intraday_data)
except Exception as e:
    print(f"Error fetching intraday data: {e}")
