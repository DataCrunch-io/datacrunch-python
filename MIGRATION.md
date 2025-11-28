### Migration from `datacrunch` to `verda`

On November 2025 [DataCrunch company changed its name to Verda](https://verda.com/blog/datacrunch-is-changing-its-name-to-verda). Starting with version 1.17.0, `verda` is the new name for the Python package.

Original `datacrunch` package is deprecated, but we will continue maintaining it, publishing new `datacrunch` releases together with the new `verda` releases using the same version numbers.

### Migration guide

While we plan to continue maintaining `datacrunch` package, we recommend migrating to `verda`. Except for import changes, API is the same.

Follow these steps to migrate:

1. Replace `datacrunch` dependency with latest `verda`

    ```
    # if your project uses uv
    uv remove datacrunch
    uv add verda

    # if your project uses pip
    pip uninstall datacrunch
    pip install verda
    ```

2. Replace `datacrunch` module with `verda` and `DataCrunchClient` class with `VerdaClient`

    ```python
    # Before
    from datacrunch import DataCrunchClient
    from datacrunch.exceptions import APIException
    try:
        datacrunch = DataCrunchClient(...)
        datacrunch.instances.create(...)
    except APIException as exception:
        print('error', exception)

    # After
    from verda import VerdaClient
    from verda.exceptions import APIException
    try:
        verda = VerdaClient(...)
        verda.instances.create(...)
    except APIException as e:
        print('error', e)
    ```

3. Change deep imports from `datacrunch.*.*` to `verda.*`

    ```python
    # Before
    from datacrunch.InferenceClient.inference_client import AsyncStatus
    from datacrunch.instances.instances import Instance

    # After
    from verda.inference_client import AsyncStatus
    from verda.instances import Instance
    ```
