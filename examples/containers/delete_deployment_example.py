"""Example script demonstrating deleting a deployment using the DataCrunch API."""

import os
from datacrunch import DataCrunchClient

DEPLOYMENT_NAME = 'sglang-deployment-example-20250411-160652'

# Get confidential values from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Initialize client with inference key
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Register signal handlers for cleanup
datacrunch.containers.delete_deployment(DEPLOYMENT_NAME)
print('Deployment deleted')
