import os
import pytest
from dotenv import load_dotenv
from datacrunch.datacrunch import DataCrunchClient

"""
Make sure to run the server and the account has enough balance before running the tests
"""

BASE_URL = "http://localhost:3010/v1"

# Load env variables, make sure there's an env file with valid client credentials
load_dotenv()
CLIENT_SECRET = os.getenv('DATACRUNCH_CLIENT_SECRET')
CLIENT_ID = os.getenv('DATACRUNCH_CLIENT_ID')


@pytest.fixture
def datacrunch_client():
    return DataCrunchClient(CLIENT_ID, CLIENT_SECRET, BASE_URL)
