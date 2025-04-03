import os
from datacrunch import DataCrunchClient

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Create datcrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Get some volume type constants
NVMe = datacrunch.constants.volume_types.NVMe
HDD = datacrunch.constants.volume_types.HDD

EXISTING_OS_VOLUME_ID = '81e45bf0-5da2-412b-97d7-c20a7564fca0'
EXAMPLE_VOLUME_ID = '225dde24-ae44-4787-9224-2b9f56f44394'
EXAMPLE_INSTANCE_ID = '1eeabba4-caf7-4b4a-9143-0107034cc7f5'

# Get all SSH keys
ssh_keys = datacrunch.ssh_keys.get()

# Create instance with extra attached volumes
instance_with_extra_volumes = datacrunch.instances.create(instance_type='1V100.6V',
                                                          image='ubuntu-24.04-cuda-12.8-open-docker',
                                                          ssh_key_ids=ssh_keys,
                                                          hostname='example',
                                                          description='example instance',
                                                          volumes=[
                                                              {"type": HDD, "name": "volume-1",
                                                                      "size": 95},
                                                              {"type": NVMe,
                                                               "name": "volume-2", "size": 95}
                                                          ])

# Create instance with custom OS volume size and name
instance_with_custom_os_volume = datacrunch.instances.create(instance_type='1V100.6V',
                                                             image='ubuntu-24.04-cuda-12.8-open-docker',
                                                             ssh_key_ids=ssh_keys,
                                                             hostname='example',
                                                             description='example instance',
                                                             os_volume={
                                                                 "name": "OS volume",
                                                                 "size": 95
                                                             })

# Create instance with existing OS volume as an image
instance_with_existing_os_volume = datacrunch.instances.create(instance_type='1V100.6V',
                                                               image=EXISTING_OS_VOLUME_ID,
                                                               ssh_key_ids=ssh_keys,
                                                               hostname='example',
                                                               description='example instance')

# Delete instance AND OS volume (the rest of the volumes would be detached)
datacrunch.instances.action(instance_id=EXAMPLE_INSTANCE_ID,
                            action=datacrunch.constants.instance_actions.DELETE)

# Delete instance WITHOUT deleting the OS volume (will detach all volumes of the instance)
datacrunch.instances.action(instance_id=EXAMPLE_INSTANCE_ID,
                            action=datacrunch.constants.instance_actions.DELETE,
                            volume_ids=[])


# Delete instance and one of it's volumes (will delete one volume, detach the rest)
datacrunch.instances.action(instance_id=EXAMPLE_INSTANCE_ID,
                            action=datacrunch.constants.instance_actions.DELETE,
                            volume_ids=[EXAMPLE_VOLUME_ID])
