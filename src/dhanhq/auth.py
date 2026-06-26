import json
import logging
import webbrowser

import requests

from .dhan_http import DhanHTTP

logger = logging.getLogger(__name__)


class DhanLogin:
    """
    Class to handle authentication and access token generation for DhanHQ API.
    """
    AUTH_BASE_URL = "https://auth.dhan.co"
    API_BASE_URL = "https://api.dhan.co/v2"

    def __init__(self, client_id):
        self.client_id = client_id

    def _parse_json(self, response):
        """Parse response JSON, raising ValueError on malformed body."""
        try:
            return response.json()
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Non-JSON response from server (HTTP {response.status_code}): {response.text[:200]}") from e

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
        params = {"client_id": self.client_id}
        headers = {"app_id": app_id, "app_secret": app_secret}

        try:
            response = requests.post(url, params=params, headers=headers, verify=True)
            response_json = self._parse_json(response)

            if response.status_code == 200 and response_json.get("status") == "success":
                consent_app_id = response_json.get("consentAppId")
                login_url = f"{self.AUTH_BASE_URL}/login/consentApp-login?consentAppId={consent_app_id}"
                logger.info("Opening browser for login: %s", login_url)
                webbrowser.open(login_url)
                return consent_app_id
            else:
                logger.error("Failed to generate consent: %s", response_json)
                raise PermissionError(f"Failed to generate consent: {response_json}")
        except (requests.ConnectionError, requests.Timeout) as e:
            logger.error("Network error in generate_login_session: %s", e)
            raise ConnectionError(f"Network error during login session generation: {e}") from e

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
        params = {"tokenId": token_id}
        headers = {"app_id": app_id, "app_secret": app_secret}

        try:
            response = requests.get(url, params=params, headers=headers, verify=True)
            response_json = self._parse_json(response)

            if response.status_code == 200:
                return response_json
            else:
                logger.error("Failed to consume token ID: %s", response_json)
                raise PermissionError(f"Failed to consume token ID: {response_json}")
        except (requests.ConnectionError, requests.Timeout) as e:
            logger.error("Network error in consume_token_id: %s", e)
            raise ConnectionError(f"Network error during token consumption: {e}") from e

    def generate_token(self, pin, totp):
        """
        Generate Access Token via PIN and TOTP.

        Args:
            pin (str): User's PIN.
            totp (str): User's TOTP.

        Returns:
            dict: The response containing the access token.
        """
        if not pin or not totp:
            raise ValueError("pin and totp must be non-empty strings")

        url = f"{self.AUTH_BASE_URL}/app/generateAccessToken"
        params = {
            "dhanClientId": self.client_id,
            "pin": pin,
            "totp": totp
        }

        try:
            response = requests.post(url, params=params, verify=True)
            response_json = self._parse_json(response)

            if response.status_code == 200:
                return response_json
            else:
                logger.error("Failed to generate token via PIN/TOTP: %s", response_json)
                raise PermissionError(f"Failed to generate token via PIN/TOTP: {response_json}")
        except (requests.ConnectionError, requests.Timeout) as e:
            logger.error("Network error in generate_token: %s", e)
            raise ConnectionError(f"Network error during token generation: {e}") from e

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
            response = requests.get(url, headers=headers, verify=True)
            response_json = self._parse_json(response)

            if response.status_code == 200:
                return response_json
            else:
                logger.error("Failed to renew token: %s", response_json)
                raise PermissionError(f"Failed to renew token: {response_json}")
        except (requests.ConnectionError, requests.Timeout) as e:
            logger.error("Network error in renew_token: %s", e)
            raise ConnectionError(f"Network error during token renewal: {e}") from e

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
            response = requests.get(url, headers=headers, verify=True)
            response_json = self._parse_json(response)

            if response.status_code == 200:
                return response_json
            else:
                logger.error("Failed to fetch user profile: %s", response_json)
                raise PermissionError(f"Failed to fetch user profile: {response_json}")
        except (requests.ConnectionError, requests.Timeout) as e:
            logger.error("Network error in user_profile: %s", e)
            raise ConnectionError(f"Network error during profile fetch: {e}") from e

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
        if ip_flag not in ('PRIMARY', 'SECONDARY'):
            raise ValueError("ip_flag must be 'PRIMARY' or 'SECONDARY'")
        dhan_client_id = dhan_client_id or self.client_id
        dhan_http = DhanHTTP(dhan_client_id, access_token)
        payload = {"ip": ip, "ipFlag": ip_flag}
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
        if ip_flag not in ('PRIMARY', 'SECONDARY'):
            raise ValueError("ip_flag must be 'PRIMARY' or 'SECONDARY'")
        dhan_client_id = dhan_client_id or self.client_id
        dhan_http = DhanHTTP(dhan_client_id, access_token)
        payload = {"ip": ip, "ipFlag": ip_flag}
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
