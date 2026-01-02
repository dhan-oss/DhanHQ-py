from dhanhq import DhanContext, dhanhq

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)
dhan = dhanhq(dhan_context)

# 2. Fetch Option Chain
# Fetch Option Chain for Nifty (13) on NSE FNO
print("\nFetching Option Chain...")
try:
    option_chain_data = dhan.option_chain(
        under_security_id=13,
        under_exchange_segment="IDX_I", # Index Option
        expiry="2023-01-25"             # Format: YYYY-MM-DD
    )
    print(option_chain_data)
except Exception as e:
    print(f"Error fetching option chain: {e}")
