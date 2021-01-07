.. DataCrunch-Python-SDK documentation master file, created by
   sphinx-quickstart on Thu Dec 24 11:34:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DataCrunch Python SDK
=====================

Welcome to the documentation for the official DataCrunch Python SDK.

The Public API documentation is `available here <https://datacrunch.stoplight.io/docs/datacrunch-public/docs/Overview/Introduction.md>`_

The Python SDK is open-sourced and can be `found here <https://github.com/DataCrunch-io/datacrunch-python>`_

Basic Examples:
---------------

Deploy a new instance:

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
                                        image='fastai',
                                        ssh_key_ids=ssh_keys_ids,
                                        hostname='example',
                                        description='example instance')

List all existing instances, ssh keys, startup scripts:

.. code-block:: python

    instances = datacrunch.instances.get()
    keys = datacrunch.ssh_keys.get()
    scripts = datacrunch.startup_scripts.get()

List all available instance & image types (information about available os images and instances to deploy)

.. code-block:: python

    instance_types = datacrunch.instance_types.get()
    images_types = datacrunch.images.get()

.. toctree::
   :maxdepth: 4
   :hidden:

   installation
   examples
   API
   contributing
   changelog