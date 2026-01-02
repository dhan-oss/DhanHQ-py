from dhanhq import DhanContext, FullDepth

# 1. Initialize Context
client_id = "YOUR_CLIENT_ID"
access_token = "YOUR_ACCESS_TOKEN"
dhan_context = DhanContext(client_id, access_token)

# 2. Define Instruments
# Format: (ExchangeSegment, SecurityID)
instruments = [
    (1, "1333"),  # HDFC Bank (ExchangeSegment 1 = NSE)
]

# 3. Initialize Full Depth
depth_level = 20 # Can be 20 or 200
full_depth = FullDepth(dhan_context, instruments, depth_level)

# 4. Run Forever
try:
    print("Connecting to Full Depth Feed...")
    full_depth.run_forever()
    
    # In a real application, you would consume data here
    # data = full_depth.get_data()
    # print(data)
    
except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Full Depth Feed Stopped")
finally:
    full_depth.disconnect()
