from dhanhq.constants.kill_switch_status import KillSwitchStatus


class TraderControlEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def kill_switch(self, action :KillSwitchStatus) -> dict[str,str]:
        """
        Control kill switch for user, which will disable trading for current trading day.

        Args:
            action (KillSwitchStatus): 'activate' or 'deactivate' to control the kill switch.

        Returns:
            dict[str,str]: Status of Kill Switch for account.
        """
        endpoint = f'/killswitch?killSwitchStatus={action.name}'
        # ToDo: This should have been an Update request aka HTTP-PUT and not HTTP-POST
        return self.dhan_http.post(endpoint)

