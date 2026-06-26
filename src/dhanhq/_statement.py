

class Statement:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_trade_book(self):
        """
        Retrieve a list of all trades executed in a day.

        Returns:
            dict: The response containing trade book data.
        """
        return self.dhan_http.get('/trades')

    def get_trade_by_order(self, order_id):
        """
        Retrieve trades for a specific order.

        Args:
            order_id (str): The ID of the order to retrieve trades for.

        Returns:
            dict: The response containing trade data for the order.
        """
        if not order_id:
            raise ValueError("order_id must be provided")
        return self.dhan_http.get(f'/trades/{order_id}')

    def get_trade_history(self, from_date, to_date, page_number=0):
        """
        Retrieve the trade history for a specific date range.

        Args:
            from_date (str): The start date for the trade history.
            to_date (str): The end date for the trade history.
            page_number (int): The page number for pagination.

        Returns:
            dict: The response containing trade history data.
        """
        endpoint = f'/trades/{from_date}/{to_date}/{page_number}'
        return self.dhan_http.get(endpoint)

    def ledger_report(self, from_date, to_date):
        """
        Retrieve the ledger details for a specific date range.

        Args:
            from_date (str): The start date for the trade history.
            to_date (str): The end date for the trade history.

        Returns:
            dict: The response containing ledger details data.
        """
        endpoint = f'/ledger?from-date={from_date}&to-date={to_date}'
        return self.dhan_http.get(endpoint)
