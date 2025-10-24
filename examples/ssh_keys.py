import os
from datacrunch import DataCrunchClient

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Create datcrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Create new SSH key
public_key = (
    'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI0qq2Qjt5GPi7DKdcnBHOkvk8xNsG9dA607tnWagOkHC test_key'
)
ssh_key = datacrunch.ssh_keys.create('my test key', public_key)

# Print new key id, name, public key
print(ssh_key.id)
print(ssh_key.name)
print(ssh_key.public_key)

# Get all keys
all_ssh_keys = datacrunch.ssh_keys.get()

# Get single key by id
some_ssh_key = datacrunch.ssh_keys.get_by_id(ssh_key.id)

# Delete ssh key by id
datacrunch.ssh_keys.delete_by_id(ssh_key.id)
