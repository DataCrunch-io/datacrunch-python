# DataCrunch Python SDK

The official DataCrunch.io python SDK.

DataCrunch's Public API documentation [is available here](https://datacrunch.stoplight.io/docs/datacrunch-public/docs/Overview/Introduction.md).

## Getting Started - Using the SDK:

- Install via pip:

  ```bash
  pip3 install datacrunch
  ```

- Add the client secret to an environment variable (don't want it to be hardcoded):

  Linux (bash):

  ```bash
  export DATACRUNCH_CLIENT_SECRET=Z4CZq02rdwdB7ISV0k4Z2gtwAFKiyvr2U1l0KDIeYi
  ```

  Other platforms:
  https://en.wikipedia.org/wiki/Environment_variable

- Example for creating a new instance:

  ```python
  import os
  from datacrunch import DataCrunchClient

  # Get client secret from environment variable
  CLIENT_SECRET = os.environ['DATACRUNCH_CLIENT_SECRET']
  CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'

  # Create datcrunch client
  datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

  # Get all SSH keys
  ssh_keys = datacrunch.ssh_keys.get()

  # Create a new instance
  instance = datacrunch.instances.create(instance_type='1V100.6V',
                                        image='fastai',
                                        ssh_key_ids=ssh_keys,
                                        hostname='example',
                                        description='example instance')

  # Delete instance
  datacrunch.instances.action(instance.id, datacrunch.actions.DELETE)
  ```

  More examples can be found in the `/examples` folder or in the documentation.

## Development

### Setting up the local development environment

- Clone the repository:

  ```bash
  git clone
  ```

- Create local virtual environment:

  ```bash
  python3 -m venv datacrunch_env && source .datacrunch_env/bin/activate
  ```

  or if using [fish shell](https://fishshell.com/):

  ```fish
  python3 -m venv datacrunch_env && source .datacrunch_env/bin/activate.fish
  ```

- Install Dependencies:

  ```bash
  pip3 install -e
  ```

### Running Tests

We use pytest for testing.

- To execute all tests

  ```bash
  pytest
  ```

- To execute a single test file

  ```bash
  pytest ./tests/unit_tests/test_file.py
  ```

### Generating the documentation

```bash
cd docs
make html
```

### Style Guide

Use autopep8 for auto code formatting:

```bash
# Install
pip3 install autopep8

# Apply to an entire directory
autopep8 directory_name --recursive --in-place --pep8-passes 2000 --verbose

# Or a single file
autopep8 file.py --in-place
```

## Contact

You can [contact us here](https://datacrunch.io/contact/), or send a message / open an issue in the repo.
