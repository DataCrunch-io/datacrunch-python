"""Example script demonstrating how to update scaling options for a container deployment.

This script shows how to update scaling configurations for an existing container deployment on DataCrunch.
"""

import os

from datacrunch import DataCrunchClient
from datacrunch.exceptions import APIException
from datacrunch.containers.containers import (
    ScalingOptions,
    ScalingPolicy,
    ScalingTriggers,
    QueueLoadScalingTrigger,
    UtilizationScalingTrigger
)

# Configuration - replace with your deployment name
DEPLOYMENT_NAME = "my-deployment"

# Environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')


def check_deployment_exists(client: DataCrunchClient, deployment_name: str) -> bool:
    """Check if a deployment exists.

    Args:
        client: DataCrunch API client
        deployment_name: Name of the deployment to check

    Returns:
        bool: True if deployment exists, False otherwise
    """
    try:
        client.containers.get_by_name(deployment_name)
        return True
    except APIException as e:
        print(f"Error: {e}")
        return False


def update_deployment_scaling(client: DataCrunchClient, deployment_name: str) -> None:
    """Update scaling options using the dedicated scaling options API.

    Args:
        client: DataCrunch API client
        deployment_name: Name of the deployment to update
    """
    try:
        # Create scaling options using ScalingOptions dataclass
        scaling_options = ScalingOptions(
            min_replica_count=1,
            max_replica_count=5,
            scale_down_policy=ScalingPolicy(
                delay_seconds=600),  # Longer cooldown period
            scale_up_policy=ScalingPolicy(delay_seconds=60),  # Quick scale-up
            queue_message_ttl_seconds=500,
            concurrent_requests_per_replica=1,
            scaling_triggers=ScalingTriggers(
                queue_load=QueueLoadScalingTrigger(threshold=1.0),
                cpu_utilization=UtilizationScalingTrigger(
                    enabled=True,
                    threshold=75
                ),
                gpu_utilization=UtilizationScalingTrigger(
                    enabled=False  # Disable GPU utilization trigger
                )
            )
        )

        # Update scaling options
        updated_options = client.containers.update_scaling_options(
            deployment_name, scaling_options)
        print(f"Updated deployment scaling options")
        print(f"New min replicas: {updated_options.min_replica_count}")
        print(f"New max replicas: {updated_options.max_replica_count}")
        print(
            f"CPU utilization trigger enabled: {updated_options.scaling_triggers.cpu_utilization.enabled}")
        print(
            f"CPU utilization threshold: {updated_options.scaling_triggers.cpu_utilization.threshold}%")
    except APIException as e:
        print(f"Error updating scaling options: {e}")


def main() -> None:
    """Main function demonstrating scaling updates."""
    try:
        # Check required environment variables
        if not DATACRUNCH_CLIENT_ID or not DATACRUNCH_CLIENT_SECRET:
            print(
                "Please set DATACRUNCH_CLIENT_ID and DATACRUNCH_CLIENT_SECRET environment variables")
            return

        # Initialize client
        client = DataCrunchClient(
            DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

        # Verify deployment exists
        if not check_deployment_exists(client, DEPLOYMENT_NAME):
            print(f"Deployment {DEPLOYMENT_NAME} does not exist.")
            return

        # Update scaling options using the API
        update_deployment_scaling(client, DEPLOYMENT_NAME)

        # Get current scaling options
        scaling_options = client.containers.get_scaling_options(
            DEPLOYMENT_NAME)
        print(f"\nCurrent scaling configuration:")
        print(f"Min replicas: {scaling_options.min_replica_count}")
        print(f"Max replicas: {scaling_options.max_replica_count}")
        print(
            f"Scale-up delay: {scaling_options.scale_up_policy.delay_seconds} seconds")
        print(
            f"Scale-down delay: {scaling_options.scale_down_policy.delay_seconds} seconds")

        print("\nScaling update completed successfully.")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
