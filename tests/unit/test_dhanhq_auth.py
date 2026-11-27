from unittest.mock import Mock, patch

import pytest
import requests

from dhanhq import DhanHTTP, DhanLogin


@pytest.mark.parametrize("method,args,verb", [
    ("generate_login_session", ("app_id", "app_secret"), "post"),
    ("consume_token_id", ("token_id", "app_id", "app_secret"), "get"),
    ("generate_token", ("pin", "totp"), "post"),
    ("renew_token", ("access_token",), "get"),
    ("user_profile", ("access_token",), "get"),
])
@pytest.mark.parametrize("times_out", [False, True])
def test_auth_request_timeout_and_response_contract(method, args, verb, times_out):
    data = {"status": "success", "consentAppId": "consent_id", "accessToken": "token"}
    response = Mock(status_code=200)
    response.json.return_value = data
    with patch(f"dhanhq.auth.requests.{verb}", return_value=response) as request:
        with patch("dhanhq.auth.webbrowser.open"):
            login = DhanLogin("test_client_id")
            if times_out:
                request.side_effect = requests.exceptions.Timeout("request timed out")
                with pytest.raises(requests.exceptions.Timeout):
                    getattr(login, method)(*args)
            else:
                result = getattr(login, method)(*args)
                assert result == ("consent_id" if method == "generate_login_session" else data)
    request.assert_called_once()
    assert request.call_args.kwargs["timeout"] == DhanHTTP.HTTP_DEFAULT_TIME_OUT
