
class TraderControl:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def kill_switch(self, action):
        """
        Control kill switch for user, which will disable trading for current trading day.

        Args:
            action (str): 'activate' or 'deactivate' to control the kill switch.

        Returns:
            dict: Status of Kill Switch for account.

        Raises:
            ValueError: If action parameter is missing or invalid.
        """
        
        if not action:
            return {
                'status': 'failure',
                'remarks': 'action parameter is required',
                'data': ''
            }

        action = action.upper()

        if action not in ['ACTIVATE', 'DEACTIVATE']:
            return {
                'status': 'failure',
                'remarks': f"Invalid action '{action}'. Must be 'ACTIVATE' or 'DEACTIVATE'",
                'data': ''
            }

        endpoint = f'/killswitch?killSwitchStatus={action}'
        return self.dhan_http.post(endpoint, {})

    def status_kill_switch(self):
        """
        Retrieve the status of the kill switch for the account.

        Returns:
            dict: Status of Kill Switch for account.
        """
        endpoint = '/killswitch'
        return self.dhan_http.get(endpoint)

    def set_pnl_exit(self, profit_value, loss_value, product_type, enable_kill_switch=False):
        """
        Configure automatic exit rules based on cumulative profit or loss thresholds.

        Args:
            profit_value (float): Target profit amount in absolute value terms (₹), not percentage.
            loss_value (float): Target loss amount in absolute value terms (₹), not percentage.
            product_type (list): List of product types to apply the rule to, e.g. ['INTRADAY', 'DELIVERY'].
            enable_kill_switch (bool): Activate the kill switch when triggered. Defaults to False.

        Returns:
            dict: The response containing the status of the P&L exit configuration.
        """
        payload = {
            "profitValue": float(profit_value),
            "lossValue": float(loss_value),
            "productType": product_type,
            "enableKillSwitch": enable_kill_switch
        }
        return self.dhan_http.post('/pnlExit', payload)

    def get_pnl_exit(self):
        """
        Fetch the currently active P&L based exit configuration.

        Returns:
            dict: The response containing the current P&L exit configuration.
        """
        return self.dhan_http.get('/pnlExit')

    def stop_pnl_exit(self):
        """
        Disable the active P&L based exit configuration.

        Returns:
            dict: The response containing the status of the operation.
        """
        return self.dhan_http.delete('/pnlExit')
