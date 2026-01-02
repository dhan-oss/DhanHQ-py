from dhanhq import DhanLogin

# Initialize DhanLogin
client_id = "YOUR_CLIENT_ID"
dhan_login = DhanLogin(client_id)

# Method 1: OAuth Flow
def oauth_login():
    app_id = "YOUR_APP_ID" # API Key
    app_secret = "YOUR_APP_SECRET" # API Secret
    
    # Step 1 & 2: Generate Consent and Open Browser
    consent_id = dhan_login.generate_login_session(app_id, app_secret)
    print(f"Consent ID: {consent_id}")
    print("Browser opened. Please login and copy the Token ID from the redirect URL.")
    
    # Step 3: Consume Token ID (After user logs in and gets Token ID)
    token_id = input("Enter Token ID from redirect URL: ")
    access_token_data = dhan_login.consume_token_id(token_id, app_id, app_secret)
    print(f"Access Token Data: {access_token_data}")

# Method 2: PIN & TOTP Flow
def pin_totp_login():
    pin = "YOUR_PIN"
    totp = "YOUR_TOTP"
    
    access_token_data = dhan_login.generate_token(pin, totp)
    print(f"Access Token Data: {access_token_data}")


# Method 3: IP Management
def ip_management(access_token):
    # Set Primary IP
    response = dhan_login.set_ip(access_token, "10.200.10.10", "PRIMARY")
    print(f"Set IP Response: {response}")

    # Modify Primary IP
    response = dhan_login.modify_ip(access_token, "10.200.10.11", "PRIMARY")
    print(f"Modify IP Response: {response}")

    # Get Configured IPs
    ip_list = dhan_login.get_ip(access_token)
    print(f"IP List: {ip_list}")

if __name__ == "__main__":
    # Uncomment the flow you want to test
    # oauth_login()
    # pin_totp_login()
    pass
