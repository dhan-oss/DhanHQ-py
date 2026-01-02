from dhanhq import dhanhq,DhanContext
import logging

logging.basicConfig(level=logging.DEBUG)

dhan_context = DhanContext("client_id","access_token")
dhan = dhanhq(dhan_context)

# Fetch ledger report of an account for a given time period
print(dhan.ledger_report("2025-10-01", "2025-11-01"))

# Fetch trade history for a given time period
print(dhan.get_trade_history("2025-10-01", "2025-11-01", 0))