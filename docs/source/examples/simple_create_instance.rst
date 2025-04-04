Simple Create Instance
======================

.. code-block:: python

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
                                        image='ubuntu-24.04-cuda-12.8-open-docker',
                                        ssh_key_ids=ssh_keys_ids,
                                        hostname='example',
                                        description='example instance')

    # Delete instance
    datacrunch.instances.action(instance.id, datacrunch.actions.DELETE)
        