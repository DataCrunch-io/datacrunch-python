import os
from datacrunch import DataCrunchClient

# Get client secret from environment variable
CLIENT_SECRET = os.environ['DATACRUNCH_CLIENT_SECRET']
CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'

# Create datcrunch client
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

# Get all SSH keys
ssh_keys = datacrunch.ssh_keys.get()

# Create a new instance
instance = datacrunch.instances.create(instance_type='1V100.6V',
                                       image='fastai',
                                       ssh_key_ids=ssh_keys,
                                       hostname='example',
                                       description='example instance')

# Delete instance
datacrunch.instances.action(instance.id, datacrunch.actions.DELETE)
