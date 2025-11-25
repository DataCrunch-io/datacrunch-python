Advanced Create Instance
========================

.. code-block:: python

    import os
    from verda import DataCrunchClient
    from verda.exceptions import APIException

    """
    In this hypothetical example, we check if we have enough balance
    to deploy an 8V100.48V instance for a week.
    If there's not enough balance, we deploy a 4V100.20V instance.

    This example uses the balance service to check the current balance,
    the instace_types service to check instance type details (price per hour)

    We also perform other basic tasks such as creating the client and adding a new SSH key.
    """

    # The instance types we want to deploy
    INSTANCE_TYPE_8V = '8V100.48V'
    INSTANCE_TYPE_4V = '4V100.20V'

    # Arbitrary duration for the example
    DURATION = 24 * 7  # one week

    # Get client secret from environment variable
    CLIENT_SECRET = os.environ['VERDA_CLIENT_SECRET']
    CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'  # Replace with your client ID

    try:
        # Create datcrunch client
        datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

        # Create new SSH key
        public_key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI0qq2Qjt5GPi7DKdcnBHOkvk8xNsG9dA607tnWagOkHC test_key'
        ssh_key = datacrunch.ssh_keys.create('my test key', public_key)

        # Get all SSH keys
        ssh_keys = datacrunch.ssh_keys.get()
        ssh_keys_ids = list(map(lambda ssh_key: ssh_key.id, ssh_keys))

        # Get our current balance
        balance = datacrunch.balance.get()
        print(balance.amount)

        # Get instance types
        instance_types = datacrunch.instance_types.get()

        # Deploy 8V instance if enough balance for a week, otherwise deploy a 4V
        for instance_details in instance_types:
            if instance_details.instance_type == INSTANCE_TYPE_8V:
                price_per_hour = instance_details.price_per_hour

                if price_per_hour * DURATION < balance.amount:
                    # Deploy a new 8V instance
                    instance = datacrunch.instances.create(instance_type=INSTANCE_TYPE_8V,
                                                        image='ubuntu-24.04-cuda-12.8-open-docker',
                                                        ssh_key_ids=ssh_keys_ids,
                                                        hostname='example',
                                                        description='large instance'
                                                        os_volume={
                                                            "name": "Large OS volume",
                                                            "size": 95
                                                        })
                else:
                    # Deploy a new 4V instance
                    instance = datacrunch.instances.create(instance_type=INSTANCE_TYPE_4V,
                                                        image='ubuntu-24.04-cuda-12.8-open-docker',
                                                        ssh_key_ids=ssh_keys_ids,
                                                        hostname='example',
                                                        description='medium instance')
    except APIException as exception:
        print(exception)
