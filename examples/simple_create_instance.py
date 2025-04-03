import os
from datacrunch import DataCrunchClient

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Create datcrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Get all SSH keys id's
ssh_keys = datacrunch.ssh_keys.get()
ssh_keys_ids = list(map(lambda ssh_key: ssh_key.id, ssh_keys))

# Create a new instance
instance = datacrunch.instances.create(instance_type='1V100.6V',
                                       image='ubuntu-24.04-cuda-12.8-open-docker',
                                       ssh_key_ids=ssh_keys_ids,
                                       hostname='example',
                                       description='example instance')

# Delete instance
datacrunch.instances.action(
    instance.id, datacrunch.constants.instance_actions.DELETE)
