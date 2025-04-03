import os
from datacrunch import DataCrunchClient
from typing import List
from datacrunch.containers.containers import ComputeResource

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')


def list_all_compute_resources(client: DataCrunchClient) -> List[ComputeResource]:
    """List all available compute resources.

    Args:
        client (DataCrunchClient): The DataCrunch API client.

    Returns:
        List[ComputeResource]: List of all compute resources.
    """
    return client.containers.get_compute_resources()


def list_available_compute_resources(client: DataCrunchClient) -> List[ComputeResource]:
    """List only the available compute resources.

    Args:
        client (DataCrunchClient): The DataCrunch API client.

    Returns:
        List[ComputeResource]: List of available compute resources.
    """
    all_resources = client.containers.get_compute_resources()
    return [r for r in all_resources if r.is_available]


def list_compute_resources_by_size(client: DataCrunchClient, size: int) -> List[ComputeResource]:
    """List compute resources filtered by size.

    Args:
        client (DataCrunchClient): The DataCrunch API client.
        size (int): The size to filter by.

    Returns:
        List[ComputeResource]: List of compute resources with the specified size.
    """
    all_resources = client.containers.get_compute_resources()
    return [r for r in all_resources if r.size == size]


def main():
    # Initialize the client with your credentials
    datacrunch = DataCrunchClient(
        DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

    # Example 1: List all compute resources
    print("All compute resources:")
    all_resources = list_all_compute_resources(datacrunch)
    for resource in all_resources:
        print(
            f"Name: {resource.name}, Size: {resource.size}, Available: {resource.is_available}")

    # Example 2: List available compute resources
    print("Available compute resources:")
    available_resources = list_available_compute_resources(datacrunch)
    for resource in available_resources:
        print(f"Name: {resource.name}, Size: {resource.size}")

    # Example 3: List compute resources of size 8
    print("Compute resources with size 8:")
    size_8_resources = list_compute_resources_by_size(datacrunch, 8)
    for resource in size_8_resources:
        print(f"Name: {resource.name}, Available: {resource.is_available}")


if __name__ == "__main__":
    main()
