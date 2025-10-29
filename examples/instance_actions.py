import os
import time

from datacrunch import DataCrunchClient
from datacrunch.exceptions import APIException

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Create datcrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Get all SSH keys
ssh_keys = datacrunch.ssh_keys.get()
ssh_keys_ids = [ssh_key.id for ssh_key in ssh_keys]

# Create a new 1V100.6V instance
instance = datacrunch.instances.create(
    instance_type='1V100.6V',
    image='ubuntu-22.04-cuda-12.0-docker',
    ssh_key_ids=ssh_keys_ids,
    hostname='example',
    description='example instance',
)

print(instance.id)

# Try to shutdown instance right away,
# encounter an error (because it's still provisioning)
try:
    datacrunch.instances.action(instance.id, datacrunch.constants.instance_actions.SHUTDOWN)
except APIException as exception:
    print(exception)  # we were too eager...

# Wait until instance is running (check every 30sec), only then shut it down
while instance.status != datacrunch.constants.instance_status.RUNNING:
    time.sleep(30)
    instance = datacrunch.instances.get_by_id(instance.id)

# Shutdown!
try:
    datacrunch.instances.action(instance.id, datacrunch.constants.instance_actions.SHUTDOWN)
except APIException as exception:
    print(exception)  # no exception this time

# Wait until instance is offline (check every 30sec), only then hibernate
while instance.status != datacrunch.constants.instance_status.OFFLINE:
    time.sleep(30)
    instance = datacrunch.instances.get_by_id(instance.id)

# Hibernate the instance
try:
    datacrunch.instances.action(instance.id, datacrunch.constants.instance_actions.HIBERNATE)
except APIException as exception:
    print(exception)
