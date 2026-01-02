
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
