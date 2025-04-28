import time
import os
from datacrunch import DataCrunchClient
from datacrunch.constants import Locations, InstanceStatus

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
                                       image='ubuntu-22.04-cuda-12.0-docker',
                                       location=Locations.FIN_01,
                                       ssh_key_ids=ssh_keys_ids,
                                       hostname='example',
                                       description='example instance')

# Wait for instance to enter running state
while instance.status != InstanceStatus.RUNNING:
    time.sleep(0.5)
    instance = datacrunch.instances.get_by_id(instance.id)

print(instance)

# Delete instance
datacrunch.instances.action(
    instance.id, datacrunch.constants.instance_actions.DELETE)
