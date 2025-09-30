
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
        """
        action = action.upper()
        endpoint = f'/killswitch?killSwitchStatus={action}'
        payload = {}
        return self.dhan_http.post(endpoint, payload)
