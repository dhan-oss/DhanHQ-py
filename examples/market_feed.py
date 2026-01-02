from dhanhq import DhanContext, MarketFeed

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)

# 2. Define Instruments
# Format: (ExchangeSegment, SecurityID, InstrumentType)
instruments = [
    (MarketFeed.NSE, "1333", MarketFeed.Ticker),  # HDFC Bank Ticker
    (MarketFeed.NSE, "1333", MarketFeed.Quote),   # HDFC Bank Quote
    (MarketFeed.NSE, "1333", MarketFeed.Full),    # HDFC Bank Full Depth
]

# 3. Initialize Market Feed
version = "v2" # Recommended version
market_feed = MarketFeed(dhan_context, instruments, version)

# 4. Run Forever
try:
    print("Connecting to Market Feed...")
    market_feed.run_forever()
    
    # In a real application, you would consume data here
    # data = market_feed.get_data()
    # print(data)
    
except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Market Feed Stopped")
finally:
    market_feed.disconnect()
