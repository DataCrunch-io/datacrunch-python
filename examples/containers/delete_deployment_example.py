"""Example script demonstrating deleting a deployment using the DataCrunch API."""

import os

from verda import VerdaClient

DEPLOYMENT_NAME = 'sglang-deployment-example-20250411-160652'

# Get confidential values from environment variables
CLIENT_ID = os.environ.get('VERDA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('VERDA_CLIENT_SECRET')

# Initialize client with inference key
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

# Register signal handlers for cleanup
datacrunch.containers.delete_deployment(DEPLOYMENT_NAME)
print('Deployment deleted')
