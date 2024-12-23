import logging

from dhanhq.dhan_http import DhanHTTP
#from dhanhq.dhan_websocket import DhanHQWebSocket # If you have a WebSocket class

class DhanContext:
    def __init__(self, client_id, access_token, disable_ssl=False, pool=None):
        try:
            self.client_id = client_id
            self.access_token = access_token
            self.dhan_http = DhanHTTP(client_id, access_token, disable_ssl, pool)
            # self.websocket_connection = DhanWebSocket(client_id, access_token) # Initialize websocket connection
        except Exception as e:
            logging.error('Exception in dhanhq>>init : %s', e)

    def get_dhan_http(self):
        return self.dhan_http

    #def get_websocket_connection(self):
    #    return self.websocket_connection

