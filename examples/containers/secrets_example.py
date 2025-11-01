import os

from datacrunch import DataCrunchClient

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Initialize DataCrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# List all secrets
secrets = datacrunch.containers.get_secrets()
print('Available secrets:')
for secret in secrets:
    print(f'- {secret.name} (created at: {secret.created_at})')

# Create a new secret
secret_name = 'my-api-key'
secret_value = 'super-secret-value'
datacrunch.containers.create_secret(name=secret_name, value=secret_value)
print(f'\nCreated new secret: {secret_name}')

# Delete a secret (with force=False by default)
datacrunch.containers.delete_secret(secret_name)
print(f'\nDeleted secret: {secret_name}')

# Delete a secret with force=True (will delete even if secret is in use)
secret_name = 'another-secret'
datacrunch.containers.create_secret(name=secret_name, value=secret_value)
datacrunch.containers.delete_secret(secret_name, force=True)
print(f'\nForce deleted secret: {secret_name}')
