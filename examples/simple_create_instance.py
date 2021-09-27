import os
from datacrunch import DataCrunchClient

# Get client secret from environment variable
CLIENT_SECRET = os.environ['DATACRUNCH_CLIENT_SECRET']
CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'  # Replace with your client ID

# Create datcrunch client
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

# Get all SSH keys id's
ssh_keys = datacrunch.ssh_keys.get()
ssh_keys_ids = list(map(lambda ssh_key: ssh_key.id, ssh_keys))

# Create a new instance
instance = datacrunch.instances.create(instance_type='1V100.6V',
                                       image='fastai',
                                       ssh_key_ids=ssh_keys_ids,
                                       hostname='example',
                                       description='example instance')

# Delete instance
datacrunch.instances.action(instance.id, datacrunch.constants.instance_actions.DELETE)
