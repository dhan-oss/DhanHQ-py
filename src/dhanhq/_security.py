import logging
import os
import requests
from pathlib import Path
from webbrowser import open as web_open

from dhanhq import DhanHTTP

logger = logging.getLogger(__name__)


class Security:

    """"Constants for HTTP Responses"""
    OTP_SENT = 'OTP sent'

    """CSV URL for Security ID List"""
    COMPACT_CSV_URL = 'https://images.dhan.co/api-data/api-scrip-master.csv'
    DETAILED_CSV_URL = 'https://images.dhan.co/api-data/api-scrip-master-detailed.csv'

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def _save_as_temp_html_file_and_open_in_browser(self, form_html):
        temp_web_form_html = "temp_form.html"
        try:
            with open(temp_web_form_html, "w") as f:
                f.write(form_html)
            web_open(Path.cwd().joinpath(temp_web_form_html).as_uri())
        finally:
            try:
                os.unlink(temp_web_form_html)
            except OSError:
                pass

    def generate_tpin(self):
        """
        Generate T-Pin on registered mobile number.

        Returns:
            dict: The response containing the status of T-Pin generation.
        """
        endpoint = '/edis/tpin'
        response = self.dhan_http.get(endpoint)
        if response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value:
            return {
                'status': response['status'],
                'remarks': self.OTP_SENT,
                'data': '',
            }
        else:
            return {
                'status': response['status'],
                'remarks': 'status code : ' + str(response['remarks'].get('error_code', '')),
                'data': '',
            }

    def open_browser_for_tpin(self, isin, qty, exchange, segment='EQ', bulk=False):
        """
        Opens the default web browser to enter T-Pin.

        Args:
            isin (str): The ISIN of the security.
            qty (int): The quantity of the security.
            exchange (str): The exchange where the security is listed.
            segment (str): The segment of the exchange (default is 'EQ').
            bulk (bool): Flag for bulk operations (default is False).

        Returns:
            dict: The response containing the status of the operation.
        """
        endpoint = '/edis/form'
        payload = {
            "isin": isin,
            "qty": qty,
            "exchange": exchange,
            "segment": segment,
            "bulk": bulk
        }
        response = self.dhan_http.post(endpoint, payload)
        if response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value:
            return response

        data = response['data']
        form_html = data['edisFormHtml']
        form_html = form_html.replace('\\', '')
        self._save_as_temp_html_file_and_open_in_browser(form_html)
        return response

    def edis_inquiry(self, isin):
        """
        Inquire about the eDIS status of the provided ISIN.

        Args:
            isin (str): The ISIN to inquire about.

        Returns:
            dict: The response containing inquiry results.
        """
        endpoint = f'/edis/inquire/{isin}'
        return self.dhan_http.get(endpoint)

    @staticmethod
    def fetch_security_list(mode='compact', filename='security_id_list.csv'):
        """
        Fetch CSV file from dhan based on the specified mode and save it to the current directory.

        Args:
            mode (str): The mode to fetch the CSV ('compact' or 'detailed').
            filename (str): The name of the file to save the CSV as.

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.
        """
        import pandas as pd

        # Sanitize filename to prevent path traversal
        safe_name = os.path.basename(filename)
        if not safe_name or safe_name != filename or '..' in filename:
            raise ValueError("filename must be a plain filename with no path components")
        if not safe_name.endswith('.csv'):
            raise ValueError("filename must end with .csv")

        try:
            if mode == 'compact':
                csv_url = Security.COMPACT_CSV_URL
            elif mode == 'detailed':
                csv_url = Security.DETAILED_CSV_URL
            else:
                raise ValueError("Invalid mode. Choose 'compact' or 'detailed'.")

            response = requests.get(csv_url)
            response.raise_for_status()

            with open(safe_name, 'wb') as f:
                f.write(response.content)
            df = pd.read_csv(safe_name)
            return df
        except Exception as e:
            logger.error('Exception in dhanhq>>fetch_security_list: %s', e)
            return None
