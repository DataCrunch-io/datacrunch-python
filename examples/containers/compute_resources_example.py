from datacrunch import DataCrunchClient
from typing import List
from datacrunch.containers.containers import ComputeResource


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
    client = DataCrunchClient(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Example 1: List all compute resources
    print("\nAll compute resources:")
    all_resources = list_all_compute_resources(client)
    for resource in all_resources:
        print(
            f"Name: {resource.name}, Size: {resource.size}, Available: {resource.is_available}")

    # Example 2: List available compute resources
    print("\nAvailable compute resources:")
    available_resources = list_available_compute_resources(client)
    for resource in available_resources:
        print(f"Name: {resource.name}, Size: {resource.size}")

    # Example 3: List compute resources of size 8
    print("\nCompute resources with size 8:")
    size_8_resources = list_compute_resources_by_size(client, 8)
    for resource in size_8_resources:
        print(f"Name: {resource.name}, Available: {resource.is_available}")


if __name__ == "__main__":
    main()
