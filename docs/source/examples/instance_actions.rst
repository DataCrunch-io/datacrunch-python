Instance Actions
================

.. code-block:: python

    import os
    import time
    from verda import DataCrunchClient
    from verda.exceptions import APIException


    # Get client secret from environment variable
    CLIENT_SECRET = os.environ['VERDA_CLIENT_SECRET']
    CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'  # Replace with your client ID

    # Create datcrunch client
    datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

    # Get all SSH keys
    ssh_keys = datacrunch.ssh_keys.get()
    ssh_keys_ids = list(map(lambda ssh_key: ssh_key.id, ssh_keys))

    # Create a new 1V100.6V instance
    instance = datacrunch.instances.create(instance_type='1V100.6V',
                                        image='ubuntu-24.04-cuda-12.8-open-docker',
                                        ssh_key_ids=ssh_keys_ids,
                                        hostname='example',
                                        description='example instance')

    print(instance.id)

    # Try to shutdown instance right away,
    # encounter an error (because it's still provisioning)
    try:
        datacrunch.instances.action(instance.id, datacrunch.actions.SHUTDOWN)
    except APIException as exception:
        print(exception)  # we were too eager...

    # Wait until instance is running (check every 30sec), only then shut it down
    while(instance.status != datacrunch.instance_status.RUNNING):
        time.sleep(30)
        instance = datacrunch.instances.get_by_id(instance.id)

    # Shutdown!
    try:
        datacrunch.instances.action(instance.id, datacrunch.actions.SHUTDOWN)
    except APIException as exception:
        print(exception)  # no exception this time

    # Wait until instance is offline (check every 30sec), only then hibernate
    while(instance.status != datacrunch.instance_status.OFFLINE):
        time.sleep(30)
        instance = datacrunch.instances.get_by_id(instance.id)

    # Hibernate the instance
    try:
        datacrunch.instances.action(instance.id, datacrunch.actions.HIBERNATE)
    except APIException as exception:
        print(exception)
