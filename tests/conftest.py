"""
This is a special file in Pytest that allows you to define fixtures that are available to all tests in your project,
without you having to import the fixture explicitly in your test files.
"""

import os
import pytest
from dotenv import load_dotenv

from dhanhq import DhanContext, dhanhq


# Load environment variables from .test.env file
load_dotenv('.test.env')

# Load Creds
API_CLIENT_ID = os.getenv('CLIENT_ID')
API_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

@pytest.fixture
def api_client_id_fixture():
    return API_CLIENT_ID

@pytest.fixture
def api_access_token_fixture():
    return API_ACCESS_TOKEN

@pytest.fixture
def dhanhq_fixture(api_client_id_fixture, api_access_token_fixture):
    dhan_context = DhanContext(api_client_id_fixture, api_access_token_fixture)
    return dhanhq(dhan_context)

@pytest.fixture
def dhanhq_obj():
    dhan_context = DhanContext("test_client_id", "test_access_token")
    return dhanhq(dhan_context)
