# DataCrunch Python SDK

[<img src='https://github.com/DataCrunch-io/datacrunch-python/workflows/Unit%20Tests/badge.svg'>](https://github.com/DataCrunch-io/datacrunch-python/actions?query=workflow%3A%22Unit+Tests%22+branch%3Amaster)
[<img src='https://github.com/DataCrunch-io/datacrunch-python/workflows/Code%20Style/badge.svg'>](https://github.com/DataCrunch-io/datacrunch-python/actions?query=workflow%3A%22Code+Style%22+branch%3Amaster)
[<img src="https://codecov.io/gh/DataCrunch-io/datacrunch-python/branch/master/graph/badge.svg?token=5X5KTYSSPK">](https://codecov.io/gh/DataCrunch-io/datacrunch-python)
[<img src='https://readthedocs.org/projects/datacrunch-python/badge/?version=latest'>](https://datacrunch-python.readthedocs.io/en/latest/)
[<img src='https://img.shields.io/github/license/DataCrunch-io/datacrunch-python'>](https://github.com/DataCrunch-io/datacrunch-python/blob/master/LICENSE)
[<img src='https://img.shields.io/pypi/v/datacrunch?logo=python'>](https://pypi.org/project/datacrunch/)
[<img src='https://img.shields.io/pypi/pyversions/datacrunch'>](https://pypi.org/project/datacrunch/)

The official [DataCrunch.io](https://datacrunch.io) Python SDK.

The SDK's documentation is available on [ReadTheDocs](https://datacrunch-python.readthedocs.io/en/latest/)

DataCrunch's Public API documentation [is available here](https://api.datacrunch.io/v1/docs).

## Getting Started - Using the SDK:

- Install via pip:

  ```bash
  pip3 install datacrunch
  ```

- Generate your client credentials - [instructions in the public API docs](https://api.datacrunch.io/v1/docs#description/quick-start-guide).


- Add your client id and client secret to an environment variable (don't want it to be hardcoded):

  Linux (bash):

  ```bash
  export DATACRUNCH_CLIENT_ID=YOUR_ID_HERE
  export DATACRUNCH_CLIENT_SECRET=YOUR_SECRET_HERE
  ```

- To enable sending inference requests from SDK you must generate an inference key - [Instructions on inference authorization](https://docs.datacrunch.io/inference/authorization)
  

- Add your inference key to an environment variable

  Linux (bash):
 
  ```bash
  export DATACRUNCH_INFERENCE_KEY=YOUR_API_KEY_HERE
  ```
  
  Other platforms:
  https://en.wikipedia.org/wiki/Environment_variable



- Example for creating a new instance:

  ```python
  import os
  from datacrunch import DataCrunchClient

  # Get credentials from environment variables
  CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
  CLIENT_SECRET = os.environ['DATACRUNCH_CLIENT_SECRET']

  # Create datcrunch client
  datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

  # Get all SSH keys
  ssh_keys = datacrunch.ssh_keys.get()
  ssh_keys = list(map(lambda key: key.id, ssh_keys))

  # Create a new instance
  instance = datacrunch.instances.create(instance_type='1V100.6V',
                                        image='ubuntu-24.04-cuda-12.8-open-docker',
                                        ssh_key_ids=ssh_keys,
                                        hostname='example',
                                        description='example instance')

  # Delete instance
  datacrunch.instances.action(instance.id, datacrunch.constants.instance_actions.DELETE)
  ```

  More examples can be found in the `/examples` folder or in the [documentation](https://datacrunch-python.readthedocs.io/en/latest/).

## Development

### Setting up the local development environment

- Clone the repository:

  ```bash
  git clone
  ```

- Create local virtual environment:

  ```bash
  python3 -m venv datacrunch_env && source ./datacrunch_env/bin/activate
  ```

  or if using [fish shell](https://fishshell.com/):

  ```fish
  python3 -m venv datacrunch_env && source ./datacrunch_env/bin/activate.fish
  ```

- Install Dependencies:

  ```bash
  pip3 install -e .[test]
  pip3 install -U pytest
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

### Local Manual Testing

Create this file in the root directory of the project:

```python
from datacrunch.datacrunch import DataCrunchClient

CLIENT_SECRET = 'secret'
CLIENT_ID = 'your-id'

# Create datcrunch client
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET, base_url='http://localhost:3001/v1')
```

### Generating the documentation

If added a new service, create a documentation template under api/services for that service.

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

You can [contact us here](https://datacrunch.io/contact), or open an issue in the repo.
