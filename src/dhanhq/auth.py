import webbrowser
import requests
import logging
from .dhan_http import DhanHTTP

class DhanLogin:
    """
    Class to handle authentication and access token generation for DhanHQ API.
    """
    AUTH_BASE_URL = "https://auth.dhan.co"
    API_BASE_URL = "https://api.dhan.co/v2"

    def __init__(self, client_id):
        self.client_id = client_id

    def generate_login_session(self, app_id, app_secret):
        """
        Step 1 & 2 of OAuth flow: Generate Consent and Open Browser for Login.
        
        Args:
            app_id (str): The API Key (App ID).
            app_secret (str): The API Secret (App Secret).
            
        Returns:
            str: The consentAppId if successful.
        """
        url = f"{self.AUTH_BASE_URL}/app/generate-consent"
        params = {
            "client_id": self.client_id
        }
        headers = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        try:
            response = requests.post(url, params=params, headers=headers)
            response_json = response.json()
            
            if response.status_code == 200 and response_json.get("status") == "success":
                consent_app_id = response_json.get("consentAppId")
                login_url = f"{self.AUTH_BASE_URL}/login/consentApp-login?consentAppId={consent_app_id}"
                print(f"Opening browser for login: {login_url}")
                webbrowser.open(login_url)
                return consent_app_id
            else:
                logging.error(f"Failed to generate consent: {response_json}")
                raise Exception(f"Failed to generate consent: {response_json}")
        except Exception as e:
            logging.error(f"Exception in generate_login_session: {e}")
            raise

    def consume_token_id(self, token_id, app_id, app_secret):
        """
        Step 3 of OAuth flow: Consume Token ID to get Access Token.
        
        Args:
            token_id (str): The token ID received after successful login (redirect).
            app_id (str): The API Key (App ID).
            app_secret (str): The API Secret (App Secret).
            
        Returns:
            dict: The response containing the access token and other details.
        """
        url = f"{self.AUTH_BASE_URL}/app/consumeApp-consent"
        params = {
            "tokenId": token_id
        }
        headers = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response_json = response.json()
            
            if response.status_code == 200:
                return response_json
            else:
                logging.error(f"Failed to consume token ID: {response_json}")
                raise Exception(f"Failed to consume token ID: {response_json}")
        except Exception as e:
            logging.error(f"Exception in consume_token_id: {e}")
            raise

    def generate_token(self, pin, totp):
        """
        Generate Access Token via PIN and TOTP.
        
        Args:
            pin (str): User's PIN.
            totp (str): User's TOTP.
            
        Returns:
            dict: The response containing the access token.
        """
        url = f"{self.AUTH_BASE_URL}/app/generateAccessToken"
        # The cURL example: curl --location --request POST 'https://auth.dhan.co/app/generateAccessToken?dhanClientId=...&pin=...&totp=...'
        # It uses POST with query parameters.
        params = {
            "dhanClientId": self.client_id,
            "pin": pin,
            "totp": totp
        }
        
        try:
            response = requests.post(url, params=params)
            response_json = response.json()
            
            # Check for success. The docs don't explicitly show the success response structure for this specific endpoint 
            # in the snippet I read, but usually it returns accessToken.
            if response.status_code == 200:
                 return response_json
            else:
                logging.error(f"Failed to generate token via PIN/TOTP: {response_json}")
                raise Exception(f"Failed to generate token via PIN/TOTP: {response_json}")
        except Exception as e:
            logging.error(f"Exception in generate_token: {e}")
            raise

    def renew_token(self, access_token):
        """
        Renew Access Token.
        
        Args:
            access_token (str): The current (expired or expiring) access token.
            
        Returns:
            dict: The response containing the new access token.
        """
        url = f"{self.API_BASE_URL}/RenewToken"
        headers = {
            "access-token": access_token,
            "dhanClientId": self.client_id
        }
        
        try:
            response = requests.get(url, headers=headers)
            response_json = response.json()
            
            if response.status_code == 200:
                return response_json
            else:
                logging.error(f"Failed to renew token: {response_json}")
                raise Exception(f"Failed to renew token: {response_json}")
        except Exception as e:
            logging.error(f"Exception in renew_token: {e}")
            raise

    def user_profile(self, access_token):
        """
        Check validity of access token and account setup.
        
        Args:
            access_token (str): The access token to verify.
            
        Returns:
            dict: The user profile details.
        """
        url = f"{self.API_BASE_URL}/profile"
        headers = {
            "access-token": access_token,
            "dhanClientId": self.client_id
        }
        
        try:
            response = requests.get(url, headers=headers)
            response_json = response.json()
            
            if response.status_code == 200:
                return response_json
            else:
                logging.error(f"Failed to fetch user profile: {response_json}")
                raise Exception(f"Failed to fetch user profile: {response_json}")
        except Exception as e:
            logging.error(f"Exception in user_profile: {e}")
            raise

    def set_ip(self, access_token, ip, ip_flag, dhan_client_id=None):
        """
        Set Primary or Secondary IP for the account.
        
        Args:
            access_token (str): The access token.
            ip (str): The IP address to whitelist.
            ip_flag (str): 'PRIMARY' or 'SECONDARY'.
            dhan_client_id (str, optional): The Dhan Client ID. Defaults to self.client_id.
            
        Returns:
            dict: The response status.
        """
        dhan_client_id = dhan_client_id or self.client_id
        dhan_http = DhanHTTP(dhan_client_id, access_token)
        
        payload = {
            "ip": ip,
            "ipFlag": ip_flag
        }
        
        return dhan_http.post('/ip/setIP', payload)

    def modify_ip(self, access_token, ip, ip_flag, dhan_client_id=None):
        """
        Modify Primary or Secondary IP for the account.
        
        Args:
            access_token (str): The access token.
            ip (str): The new IP address.
            ip_flag (str): 'PRIMARY' or 'SECONDARY'.
            dhan_client_id (str, optional): The Dhan Client ID. Defaults to self.client_id.
            
        Returns:
            dict: The response status.
        """
        dhan_client_id = dhan_client_id or self.client_id
        dhan_http = DhanHTTP(dhan_client_id, access_token)
        
        payload = {
            "ip": ip,
            "ipFlag": ip_flag
        }
        
        return dhan_http.put('/ip/modifyIP', payload)

    def get_ip(self, access_token, dhan_client_id=None):
        """
        Get the list of currently set IPs.
        
        Args:
            access_token (str): The access token.
            dhan_client_id (str, optional): The Dhan Client ID. Defaults to self.client_id.
            
        Returns:
            dict: The list of IPs and modify dates.
        """
        dhan_client_id = dhan_client_id or self.client_id
        dhan_http = DhanHTTP(dhan_client_id, access_token)
        
        return dhan_http.get('/ip/getIP')
