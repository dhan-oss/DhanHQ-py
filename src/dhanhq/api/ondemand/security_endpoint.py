from json import loads as json_loads
from pathlib import Path
from webbrowser import open as web_open
import logging
import requests

from dhanhq.api import DhanConnection
from dhanhq.http import DhanHTTP

class SecurityEndpoint:

    """"Constants for HTTP Responses"""
    OTP_SENT = 'OTP sent'

    """CSV URL for SecurityEndpoint ID List"""
    COMPACT_CSV_URL = 'https://images.dhan.co/api-data/api-scrip-master.csv'
    DETAILED_CSV_URL = 'https://images.dhan.co/api-data/api-scrip-master-detailed.csv'

    def __init__(self, dhan_context: DhanConnection):
        self.dhan_http = dhan_context.get_dhan_http()

    def _save_as_temp_html_file_and_open_in_browser(self, form_html: str) -> None:
        temp_web_form_html = "temp_form.html"
        with open(temp_web_form_html, "w") as f:
            f.write(form_html)
        web_open(Path.cwd().joinpath(temp_web_form_html).as_uri())

    def generate_tpin(self) -> str:
        """
        Generate T-Pin on registered mobile number.
        """
        endpoint = '/edis/tpin'
        self.dhan_http.get(endpoint)
        return self.OTP_SENT

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
        data = self.dhan_http.post(endpoint, payload)
        # data = json_loads(response)
        form_html = data['edisFormHtml']  # data['edisFormHtml']
        form_html = form_html.replace('\\', '')
        self._save_as_temp_html_file_and_open_in_browser(form_html)
        return data

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
            filename (str): The name of the file to save the CSV as (default is 'data.csv').

        Returns:
            pd.DataFrame: The DataFrame containing the CSV data.
        """
        import pandas as pd
        try:
            if mode == 'compact':
                csv_url = SecurityEndpoint.COMPACT_CSV_URL
            elif mode == 'detailed':
                csv_url = SecurityEndpoint.DETAILED_CSV_URL
            else:
                raise ValueError("Invalid mode. Choose 'compact' or 'detailed'.")

            response = requests.get(csv_url)
            response.raise_for_status()

            with open(filename, 'wb') as f:
                f.write(response.content)
            df = pd.read_csv(filename)
            return df
        except Exception as e:
            logging.error('Exception in dhanhq>>fetch_security_list: %s', e)
            return None
