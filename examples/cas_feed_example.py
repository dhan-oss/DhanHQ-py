from dhanhq import DhanContext, CASFeed

# Closing Auction Session (CAS) Live Feed - needs the Pro Traders Plan.
# Data is streamed during the closing auction session.

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)

# 2. Define Instruments
# Format: (ExchangeSegment, SecurityID). ExchangeSegment can be a code such as CASFeed.NSE or a name such as "NSE_EQ".
# Subscribe indices (CASFeed.IDX) to receive their indicative close values.
instruments = [
    (CASFeed.NSE, "1333"),    # HDFC Bank
    (CASFeed.BSE, "500325"),  # Reliance Industries
    (CASFeed.IDX, "13"),      # NIFTY 50
]

# 3. Initialize the CAS Live Feed
cas_feed = CASFeed(dhan_context, instruments)

# 4. Run Forever
try:
    print("Connecting to CAS Live Feed...")
    cas_feed.run_forever()

    while True:
        # A single call can return one packet (dict) or several concatenated packets (list)
        data = cas_feed.get_data()
        for packet in (data if isinstance(data, list) else [data]):
            if packet["type"] == "CAS":
                print(packet["security_id"], "IEP:", packet["IEP"],
                      "Buy:", packet["total_buy_quantity"], "Sell:", packet["total_sell_quantity"])
            else:
                print(packet)

except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("CAS Feed Stopped")
finally:
    cas_feed.close_connection()
