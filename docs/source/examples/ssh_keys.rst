SSH Keys
========

.. code-block:: python

    import os
    from datacrunch import DataCrunchClient

    # Get client secret from environment variable
    CLIENT_SECRET = os.environ['DATACRUNCH_CLIENT_SECRET']
    CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'  # Replace with your client ID

    # Create datcrunch client
    datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

    # Create new SSH key
    public_key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI0qq2Qjt5GPi7DKdcnBHOkvk8xNsG9dA607tnWagOkHC test_key'
    ssh_key = datacrunch.ssh_keys.create('my test key', public_key)

    # Print new key id, name, public key
    print(ssh_key.id)
    print(ssh_key.name)
    print(ssh_key.public_key)

    # Get all keys
    all_ssh_keys = datacrunch.ssh_keys.get()

    # Get single key by id
    some_ssh_key = datacrunch.ssh_keys.get_by_id(ssh_key.id)

    # Delete ssh key by id
    datacrunch.ssh_keys.delete_by_id(ssh_key.id)
