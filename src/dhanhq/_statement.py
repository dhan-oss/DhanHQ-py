

class Statement:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_trade_book(self, order_id=None):
        """
        Retrieve a list of all trades executed in a day.

        Args:
            order_id (str, optional): The ID of the specific order to retrieve trades for.

        Returns:
            dict: The response containing trade book data.
        """
        # ToDo: This is bad practice abusing REST principles.
        #  This should be broken into two different methods with appropriate REST convention-based URL.
        endpoint = f'/trades/{order_id if order_id is not None else ""}'
        return self.dhan_http.get(endpoint)

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
