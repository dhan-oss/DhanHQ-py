
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

        Notes:
            The method upper-cases the provided `action` and sends it to the
            killswitch endpoint. Prior validation may be performed by the
            service; this SDK method does not raise on invalid actions but
            returns the upstream response.
        """
        
        if not action:
            return {
                'status': 'failure',
                'remarks': 'action parameter is required',
                'data': ''
            }

        action = action.upper()
        endpoint = f'/killswitch?killSwitchStatus={action}'
        return self.dhan_http.post(endpoint)

    def status_kill_switch(self):
        """
        Retrieve the status of the kill switch for the account.

        Returns:
            dict: Status of Kill Switch for account.
        """
        endpoint = '/killswitch'
        return self.dhan_http.get(endpoint)
