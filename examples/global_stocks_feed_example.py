from dhanhq import DhanContext, GlobalStocksFeed

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)

# 2. Define Instruments
# Format: (ExchangeSegment, SecurityID) defaults to Trade feed, or
#         (ExchangeSegment, SecurityID, RequestCode) where RequestCode is
#         GlobalStocksFeed.SubscribeTrade (15) or GlobalStocksFeed.SubscribeOHLC (17).
instruments = [
    (GlobalStocksFeed.INX_EQ, "1234"),                                  # Trade feed
    (GlobalStocksFeed.INX_EQ, "5678", GlobalStocksFeed.SubscribeOHLC),  # OHLC feed
]

# 3. Initialize the Global Stocks Live Feed
global_feed = GlobalStocksFeed(dhan_context, instruments, auth_type=GlobalStocksFeed.AUTH_SELF)

# 4. Run Forever
try:
    print("Connecting to Global Stocks Live Feed...")
    global_feed.run_forever()

    # In a real application, you would consume data here
    # data = global_feed.get_data()
    # print(data)

except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Global Stocks Feed Stopped")
finally:
    global_feed.disconnect()
