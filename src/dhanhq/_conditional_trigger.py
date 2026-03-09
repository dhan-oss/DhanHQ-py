class ConditionalTrigger:
    """
    Interface for Conditional Trigger (alerts/orders) APIs.
    Endpoints:
      POST   /alerts/orders
      PUT    /alerts/orders/{alertId}
      DELETE /alerts/orders/{alertId}
      GET    /alerts/orders/{alertId}
      GET    /alerts/orders
    """

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def place_conditional(self, dhan_client_id, condition, orders):
        """Place a new conditional trigger alert.

        Args:
            dhan_client_id (str|int): Client id for Dhan (optional for some contexts).
            condition (dict): Condition payload as per API docs.
            orders (list): List of order objects to execute when condition meets.

        Returns:
            dict: API response from POST /alerts/orders
        """
        if not condition or not orders:
            raise ValueError("Both 'condition' and 'orders' must be provided")

        endpoint = '/alerts/orders'
        payload = {
            "dhanClientId": dhan_client_id,
            "condition": condition,
            "orders": orders
        }
        return self.dhan_http.post(endpoint, payload)

    def modify_conditional(self, alert_id, dhan_client_id, condition, orders):
        """Modify an existing conditional trigger.

        Args:
            alert_id (str): The alert id to modify.
            dhan_client_id (str|int): Client id value.
            condition (dict): Updated condition object.
            orders (list): Updated list of orders.

        Returns:
            dict: API response from PUT /alerts/orders/{alertId}
        """
        if not alert_id:
            raise ValueError("alert_id is required to modify a conditional trigger")
        endpoint = f'/alerts/orders/{alert_id}'
        payload = {
            "dhanClientId": dhan_client_id,
            "alertId": alert_id,
            "condition": condition,
            "orders": orders
        }
        return self.dhan_http.put(endpoint, payload)

    def delete_conditional(self, alert_id):
        """Delete a conditional trigger by alert id."""
        endpoint = f'/alerts/orders/{alert_id}'
        return self.dhan_http.delete(endpoint)

    def get_conditional_by_id(self, alert_id):
        """Get a conditional trigger by alert id."""
        endpoint = f'/alerts/orders/{alert_id}'
        return self.dhan_http.get(endpoint)

    def get_all_conditionals(self):
        """Retrieve all conditional triggers for the account."""
        endpoint = '/alerts/orders'
        return self.dhan_http.get(endpoint)
