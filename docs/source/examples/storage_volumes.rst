Storage Volumes
===============

.. code-block:: python

    import os
    from verda import VerdaClient

    # Get client secret from environment variable
    CLIENT_SECRET = os.environ['VERDA_CLIENT_SECRET']
    CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'  # Replace with your client ID

    # Create datcrunch client
    verda = VerdaClient(CLIENT_ID, CLIENT_SECRET)

    # Get some volume type constants
    NVMe = verda.constants.volume_types.NVMe
    HDD = verda.constants.volume_types.HDD

    # Example instance id
    INSTANCE_ID = '8705bb38-2574-454f-9967-d18b130bf5ee'

    # Get all volumes
    all_volumes = verda.volumes.get()

    # Get all attached volumes
    all_attached_volumes = verda.volumes.get(status=verda.constants.volume_status.ATTACHED)

    # Get volume by id
    random_volume = verda.volumes.get_by_id("0c41e387-3dd8-495f-a285-e861527f2f3d")

    # Create a 200 GB detached NVMe volume
    nvme_volume = verda.volumes.create(type=NVMe,
                                            name="data-storage-1",
                                            size=200)

    # Create a 500 GB HDD volume and attach it to an existing shutdown instance
    # Note: If the instance isn't shutdown an exception would be raised
    hdd_volume = verda.volumes.create(type=HDD,
                                        name="data-storage-2",
                                        size=500,
                                        instance_id=INSTANCE_ID)

    nvme_volume_id = nvme_volume.id
    hdd_volume_id = hdd_volume.id

    # attach the nvme volume to the instance
    verda.volumes.attach(nvme_volume_id, INSTANCE_ID)

    # detach both volumes from the instance
    verda.volumes.detach([nvme_volume_id, hdd_volume_id])

    # rename volume
    verda.volumes.rename(nvme_volume_id, "new-name")

    # increase volume size
    verda.volumes.increase_size(nvme_volume_id, 300)

    # delete volumes
    verda.volumes.delete([nvme_volume_id, hdd_volume_id])
