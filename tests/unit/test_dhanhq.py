from json import dumps as json_dumps
from unittest.mock import patch

import pytest

from dhanhq import DhanContext
from dhanhq.dhan_http import DhanHTTP
from dhanhq.dhanhq import dhanhq


@pytest.fixture
def dhanhq_obj():
    dhan_context = DhanContext("test_client_id", "test_access_token")
    return dhanhq(dhan_context)

class TestDhanhq_Orders:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_order_list_success(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.get_order_list()
        mock_read_request.assert_called_once_with('/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_order_by_id(self, mock_read_request, dhanhq_obj):
        order_id = "12345"
        dhanhq_obj.get_order_by_id(order_id)
        mock_read_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_order_by_correlation_id(self, mock_read_request, dhanhq_obj):
        correlation_id = "12345"
        dhanhq_obj.get_order_by_correlationID(correlation_id)
        mock_read_request.assert_called_once_with(f'/orders/external/{correlation_id}')

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_order_success(self, mock_delete_request, dhanhq_obj):
        order_id = "12345"
        dhanhq_obj.cancel_order(order_id)
        mock_delete_request.assert_called_once_with(f'/orders/{order_id}')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_order_success(self,mock_create_request,dhanhq_obj):
        endpoint = '/orders'
        security_id = 1
        exchange_segment = "exchange_segment"
        transaction_type = "transaction_type"
        quantity =100
        order_type = "order_type"
        product_type = "product_type"
        price = 123
        dhanhq_obj.place_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity='DAY', amo_time='OPEN',
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_slice_order_success(self,mock_create_request,dhanhq_obj):
        endpoint = '/orders/slicing'
        security_id = 1
        exchange_segment = "exchange_segment"
        transaction_type = "transaction_type"
        quantity =100
        order_type = "order_type"
        product_type = "product_type"
        price = 123
        dhanhq_obj.place_slice_order(security_id, exchange_segment, transaction_type, quantity,
                    order_type, product_type, price, trigger_price=0, disclosed_quantity=0,
                    after_market_order=False, validity='DAY', amo_time='OPEN',
                    bo_profit_value=None, bo_stop_loss_Value=None, tag=None)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_order_success(self,mock_update_request,dhanhq_obj):
        order_id = 123
        endpoint = f'/orders/{order_id}'
        quantity = 100
        price = 99
        trigger_price = 100
        dhanhq_obj.modify_order(order_id, "order_type", "leg_name", quantity, price,
                                trigger_price, trigger_price, "validity")
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint

class TestDhanhq_Portfolio:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_positions(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.get_positions()
        mock_read_request.assert_called_once_with('/positions')

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_holdings(self, mock_read_request, dhanhq_obj):
        dhanhq_obj.get_holdings()
        mock_read_request.assert_called_once_with('/holdings')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_convert_position(self, mock_create_request, dhanhq_obj):
        dhanhq_obj.convert_position("from_product_type", "exchange_segment", "position_type", "security_id", "convert_qty", "to_product_type")
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == '/positions/convert'

class TestDhanhq_ForeverOrder:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_forever(self,mock_read_request,dhanhq_obj):
        dhanhq_obj.get_forever()
        mock_read_request.assert_called_once_with('/forever/orders')

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_place_forever(self,mock_create_request, dhanhq_obj):
        endpoint = '/forever/orders'
        quantity = 100
        price = 108
        trigger_Price = 110
        dhanhq_obj.place_forever("security_id", "exchange_segment", "transaction_type",
                                 "product_type", "order_type", quantity, price, trigger_Price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.put")
    def test_modify_forever(self, mock_update_request, dhanhq_obj):
        order_id = 123
        endpoint = f'/forever/orders/{order_id}'
        quantity = 100
        price = 108
        trigger_price = 110
        disclosed_quantity = 555
        dhanhq_obj.modify_forever(order_id, "order_flag", "order_type", "leg_name",
                                  quantity, price, trigger_price, disclosed_quantity,"validity")
        mock_update_request.assert_called_once()
        assert mock_update_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.delete")
    def test_cancel_forever(self, mock_delete_request, dhanhq_obj):
        order_id = "123"
        endpoint = f'/forever/orders/{order_id}'
        dhanhq_obj.cancel_forever(order_id)
        mock_delete_request.assert_called_once_with(endpoint)

class TestDhanhq_ElectronicDelivery:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_generate_tpin_for_success(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = { 'status': DhanHTTP.HttpResponseStatus.SUCCESS.value, 'remarks': '', 'data': '', }
        json_response = dhanhq_obj.generate_tpin()
        mock_read_request.assert_called_once_with('/edis/tpin')
        assert json_response['remarks'] == dhanhq.OTP_SENT # ToDo: Ideally, response.data should be set so
        assert json_response['data'] == ''

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_generate_tpin_for_failure(self, mock_read_request, dhanhq_obj):
        mock_read_request.return_value = {
            'status': DhanHTTP.HttpResponseStatus.FAILURE.value,
            'remarks': {
                    'error_code': 'HTPP500',
                    'error_type': 'Internal Server Error',
                    'error_message': 'HTPP500:Internal Server Error'
                },
            'data': '', }
        json_response = dhanhq_obj.generate_tpin()
        mock_read_request.assert_called_once_with('/edis/tpin')
        assert json_response['remarks'].startswith('status code :')
        assert json_response['data'] == ''

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    @patch("dhanhq.dhanhq._save_as_temp_html_file_and_open_in_browser")
    def test_open_browser_for_tpin_success(self, mock_save_and_open, mock_create_request, dhanhq_obj):
        # print(mock_create_request)
        # print(mock_save_and_open)
        mock_create_request.return_value = {
            'status': DhanHTTP.HttpResponseStatus.SUCCESS.value,
            'data': '{"edisFormHtml": "<html></html>"}'
        }
        response = dhanhq_obj.open_browser_for_tpin('isin', 1, 'exchange')
        assert response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        mock_save_and_open.assert_called_once()

    @patch('dhanhq.dhan_http.DhanHTTP.post')
    @patch("dhanhq.dhanhq._save_as_temp_html_file_and_open_in_browser")
    def test_open_browser_for_tpin_failure(self, mock_save_and_open, mock_create_request, dhanhq_obj):
        mock_create_request.return_value = {
            'status': DhanHTTP.HttpResponseStatus.FAILURE.value,
            'data': ''
        }
        response = dhanhq_obj.open_browser_for_tpin('isin', 1, 'exchange')
        assert response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        mock_save_and_open.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_edis_inquiry(self, mock_read_request, dhanhq_obj):
        isin = "123"
        endpoint = f'/edis/inquire/{isin}'
        dhanhq_obj.edis_inquiry(isin)
        mock_read_request.assert_called_once_with(endpoint)

class TestDhanhq_TraderControls:
    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_kill_switch(self, mock_post_request, dhanhq_obj):
        action = "action"
        endpoint = f'/killswitch?killSwitchStatus={action.upper()}'
        dhanhq_obj.kill_switch(action)
        mock_post_request.assert_called_once_with(endpoint)

class TestDhanhq_Funds:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_fund_limits(self, mock_read_request, dhanhq_obj):
        endpoint = '/fundlimit'
        dhanhq_obj.get_fund_limits()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_margin_calculator(self, mock_create_request, dhanhq_obj):
        endpoint = '/margincalculator'
        quantity=100
        price = 99.99
        dhanhq_obj.margin_calculator("security_id", "exchange_segment", "transaction_type",
                                     100, "product_type", price)
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

class TestDhanhq_Statement:
    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_trade_book_without_orderid(self, mock_read_request, dhanhq_obj):
        endpoint = '/trades/'
        dhanhq_obj.get_trade_book()
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_trade_book_with_orderid(self, mock_read_request, dhanhq_obj):
        order_id = "order_id"
        endpoint = f'/trades/{order_id}'
        dhanhq_obj.get_trade_book(order_id)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_get_trade_history(self, mock_read_request, dhanhq_obj):
        from_date = "from_date"
        to_date = "to_date"
        page_number = "page_number"
        endpoint = f'/trades/{from_date}/{to_date}/{page_number}'
        dhanhq_obj.get_trade_history(from_date,to_date,page_number)
        mock_read_request.assert_called_once_with(endpoint)


    @patch("dhanhq.dhan_http.DhanHTTP.get")
    def test_ledger_report(self, mock_read_request, dhanhq_obj):
        from_date = "from_date"
        to_date = "to_date"
        endpoint = f'/ledger?from-date={from_date}&to-date={to_date}'
        dhanhq_obj.ledger_report(from_date,to_date)
        mock_read_request.assert_called_once_with(endpoint)

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_intraday_minute_data(self, mock_create_request, dhanhq_obj):
        endpoint = f'/charts/intraday'
        security_id="security_id"
        exchange_segment="exchange_segment"
        instrument_type="instrument_type"
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = { 'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        mock_create_request.assert_called_once()
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_intraday_minute_data_fails_for_bad_interval_input(self, mock_create_request, dhanhq_obj):
        security_id="security_id"
        exchange_segment="exchange_segment"
        instrument_type="instrument_type"
        from_date="from_date"
        to_date="to_date"
        interval=100
        json_response = dhanhq_obj.intraday_minute_data(security_id, exchange_segment, instrument_type, from_date, to_date, interval)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_historical_daily_data(self, mock_create_request, dhanhq_obj):
        endpoint = f'/charts/historical'
        security_id='security_id'
        exchange_segment='exchange_segment'
        instrument_type='instrument_type'
        from_date="from_date"
        to_date="to_date"
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_historical_daily_data_fails_for_bad_expiry_code(self, mock_create_request, dhanhq_obj):
        security_id='security_id'
        exchange_segment='exchange_segment'
        instrument_type='instrument_type'
        from_date="from_date"
        to_date="to_date"
        bad_expiry_code=99
        json_response = dhanhq_obj.historical_daily_data(security_id, exchange_segment, instrument_type, from_date, to_date,bad_expiry_code)
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.FAILURE.value
        mock_create_request.assert_not_called()

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_ticker_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/marketfeed/ltp'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.ticker_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_ohlc_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/marketfeed/ohlc'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.ohlc_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_quote_data(self, mock_create_request, dhanhq_obj):
        endpoint = '/marketfeed/quote'
        securities = {
            'exchange_segment1': 'security_id1',
            'exchange_segment2': 'security_id2'
        }
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.quote_data(securities)
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
        assert mock_create_request.call_args[0][1] == securities

    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_option_chain(self, mock_create_request, dhanhq_obj):
        endpoint = '/optionchain'
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.option_chain("under_security_id", "under_exchange_segment", "expiry")
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint


    @patch("dhanhq.dhan_http.DhanHTTP.post")
    def test_expiry_list(self, mock_create_request, dhanhq_obj):
        endpoint = '/optionchain/expirylist'
        mock_create_request.return_value = {'status': DhanHTTP.HttpResponseStatus.SUCCESS.value}
        json_response = dhanhq_obj.expiry_list("under_security_id", "under_exchange_segment")
        mock_create_request.assert_called_once()
        assert json_response['status'] == DhanHTTP.HttpResponseStatus.SUCCESS.value
        assert mock_create_request.call_args[0][0] == endpoint
