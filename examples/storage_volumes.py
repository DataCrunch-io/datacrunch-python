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

# Example instance id
INSTANCE_ID = '8705bb38-2574-454f-9967-d18b130bf5ee'

# Get all volumes
all_volumes = datacrunch.volumes.get()

# Get all attached volumes
all_attached_volumes = datacrunch.volumes.get(status=datacrunch.constants.volume_status.ATTACHED)

# Get volume by id
random_volume = datacrunch.volumes.get_by_id('0c41e387-3dd8-495f-a285-e861527f2f3d')

# Create a 200 GB detached NVMe volume
nvme_volume = datacrunch.volumes.create(type=NVMe, name='data-storage-1', size=200)

# Create a 500 GB HDD volume and attach it to an existing shutdown instance
# Note: If the instance isn't shutdown an exception would be raised
hdd_volume = datacrunch.volumes.create(
    type=HDD, name='data-storage-2', size=500, instance_id=INSTANCE_ID
)

nvme_volume_id = nvme_volume.id
hdd_volume_id = hdd_volume.id

# attach the nvme volume to the instance
datacrunch.volumes.attach(nvme_volume_id, INSTANCE_ID)

# detach both volumes from the instance
datacrunch.volumes.detach([nvme_volume_id, hdd_volume_id])

# rename volume
datacrunch.volumes.rename(nvme_volume_id, 'new-name')

# increase volume size
datacrunch.volumes.increase_size(nvme_volume_id, 300)

# clone volume
datacrunch.volumes.clone(nvme_volume_id)

# clone volume and give it a new name and storage type (from NVMe to HDD)
datacrunch.volumes.clone(nvme_volume_id, name='my-cloned-volume', type=HDD)

# clone multiple volumes at once
datacrunch.volumes.clone([nvme_volume_id, hdd_volume_id])

# delete volumes (move to trash for 96h, not permanent)
datacrunch.volumes.delete([nvme_volume_id, hdd_volume_id])

# get all volumes in trash
volumes_in_trash = datacrunch.volumes.get_in_trash()

# delete volumes permanently
datacrunch.volumes.delete([nvme_volume_id, hdd_volume_id], is_permanent=True)
