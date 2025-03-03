from typing import List

from pydantic import TypeAdapter

from dhanhq.constant import ExchangeSegment, PositionType, ProductType
from dhanhq.dto import Holding, Position, ConvertPositionRequest


class PortfolioEndpoint:

    def __init__(self, dhan_context):
        self.dhan_http = dhan_context.get_dhan_http()

    def get_current_holdings(self) -> list[Holding]:
        """
        Retrieve all holdings bought/sold in previous trading sessions.
        """
        dict_response = self.dhan_http.get('/holdings')
        adapter = TypeAdapter(List[Holding])
        holdings = adapter.validate_python(dict_response, context={"exclude_unset": True})
        return holdings

    def get_current_positions(self) -> list[Position]:
        """
        Retrieve a list of all open positions for the day.
        """
        dict_response = self.dhan_http.get('/positions')
        adapter = TypeAdapter(List[Position])
        positions = adapter.validate_python(dict_response, context={"exclude_unset": True})
        return positions

    def convert_position(self, convertPositionRequest: ConvertPositionRequest) -> dict:
        """
        Convert Position from Intraday to Delivery or vice versa.

        Returns:
            dict: The response containing the status of the conversion.
        """
        endpoint = '/positions/convert'
        return self.dhan_http.post(endpoint, convertPositionRequest.model_dump())

