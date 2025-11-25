import os

from verda import DataCrunchClient

# Get client secret and id from environment variables
CLIENT_ID = os.environ.get('VERDA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('VERDA_CLIENT_SECRET')

# Initialize DataCrunch client
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

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
