"""Example script demonstrating container deployment management using the DataCrunch API.

This script provides a comprehensive example of container deployment lifecycle,
including creation, monitoring, scaling, and cleanup.
"""

import os
import time

from datacrunch import DataCrunchClient
from datacrunch.exceptions import APIException
from datacrunch.containers.containers import (
    Container,
    ComputeResource,
    ScalingOptions,
    ScalingPolicy,
    ScalingTriggers,
    QueueLoadScalingTrigger,
    UtilizationScalingTrigger,
    HealthcheckSettings,
    VolumeMount,
    ContainerRegistrySettings,
    Deployment,
    VolumeMountType,
    ContainerDeploymentStatus,
)

# Configuration constants
DEPLOYMENT_NAME = "my-deployment"
CONTAINER_NAME = "my-app"


def wait_for_deployment_health(client: DataCrunchClient, deployment_name: str, max_attempts: int = 10, delay: int = 30) -> bool:
    """Wait for deployment to reach healthy status.

    Args:
        client: DataCrunch API client
        deployment_name: Name of the deployment to check
        max_attempts: Maximum number of status checks
        delay: Delay between checks in seconds

    Returns:
        bool: True if deployment is healthy, False otherwise
    """
    for attempt in range(max_attempts):
        try:
            status = client.containers.get_status(deployment_name)
            print(f"Deployment status: {status}")
            if status == ContainerDeploymentStatus.HEALTHY:
                return True
            time.sleep(delay)
        except APIException as e:
            print(f"Error checking deployment status: {e}")
            return False
    return False


def cleanup_resources(client: DataCrunchClient) -> None:
    """Clean up all created resources.

    Args:
        client: DataCrunch API client
    """
    try:
        # Delete deployment
        client.containers.delete(DEPLOYMENT_NAME)
        print("Deployment deleted")
    except APIException as e:
        print(f"Error during cleanup: {e}")


def main() -> None:
    """Main function demonstrating deployment lifecycle management."""
    try:
        # Initialize client
        client_id = os.environ.get('DATACRUNCH_CLIENT_ID')
        client_secret = os.environ.get('DATACRUNCH_CLIENT_SECRET')
        datacrunch = DataCrunchClient(client_id, client_secret)

        # Create container configuration
        container = Container(
            name=CONTAINER_NAME,
            image='nginx:latest',
            exposed_port=80,
            healthcheck=HealthcheckSettings(
                enabled=True,
                port=80,
                path="/health"
            ),
            volume_mounts=[
                VolumeMount(
                    type=VolumeMountType.SCRATCH,
                    mount_path="/data"
                )
            ]
        )

        # Create scaling configuration
        scaling_options = ScalingOptions(
            min_replica_count=1,
            max_replica_count=5,
            scale_down_policy=ScalingPolicy(delay_seconds=300),
            scale_up_policy=ScalingPolicy(delay_seconds=300),
            queue_message_ttl_seconds=500,
            concurrent_requests_per_replica=1,
            scaling_triggers=ScalingTriggers(
                queue_load=QueueLoadScalingTrigger(threshold=1),
                cpu_utilization=UtilizationScalingTrigger(
                    enabled=True,
                    threshold=80
                ),
                gpu_utilization=UtilizationScalingTrigger(
                    enabled=True,
                    threshold=80
                )
            )
        )

        # Create registry and compute settings
        registry_settings = ContainerRegistrySettings(is_private=False)
        compute = ComputeResource(name="General Compute", size=1)

        # Create deployment object
        deployment = Deployment(
            name=DEPLOYMENT_NAME,
            container_registry_settings=registry_settings,
            containers=[container],
            compute=compute,
            scaling=scaling_options,
            is_spot=False
        )

        # Create the deployment
        created_deployment = datacrunch.containers.create(deployment)
        print(f"Created deployment: {created_deployment.name}")

        # Wait for deployment to be healthy
        if not wait_for_deployment_health(datacrunch, DEPLOYMENT_NAME):
            print("Deployment health check failed")
            cleanup_resources(datacrunch)
            return

        # Update scaling configuration
        try:
            deployment = datacrunch.containers.get_by_name(DEPLOYMENT_NAME)
            # Create new scaling options with increased replica counts
            deployment.scaling = ScalingOptions(
                min_replica_count=2,
                max_replica_count=10,
                scale_down_policy=ScalingPolicy(delay_seconds=300),
                scale_up_policy=ScalingPolicy(delay_seconds=300),
                queue_message_ttl_seconds=500,
                concurrent_requests_per_replica=1,
                scaling_triggers=ScalingTriggers(
                    queue_load=QueueLoadScalingTrigger(threshold=1),
                    cpu_utilization=UtilizationScalingTrigger(
                        enabled=True,
                        threshold=80
                    ),
                    gpu_utilization=UtilizationScalingTrigger(
                        enabled=True,
                        threshold=80
                    )
                )
            )
            updated_deployment = datacrunch.containers.update(
                DEPLOYMENT_NAME, deployment)
            print(f"Updated deployment scaling: {updated_deployment.name}")
        except APIException as e:
            print(f"Error updating scaling options: {e}")

        # Demonstrate deployment operations
        try:
            # Pause deployment
            datacrunch.containers.pause(DEPLOYMENT_NAME)
            print("Deployment paused")
            time.sleep(60)

            # Resume deployment
            datacrunch.containers.resume(DEPLOYMENT_NAME)
            print("Deployment resumed")

            # Restart deployment
            datacrunch.containers.restart(DEPLOYMENT_NAME)
            print("Deployment restarted")

            # Purge queue
            datacrunch.containers.purge_queue(DEPLOYMENT_NAME)
            print("Queue purged")
        except APIException as e:
            print(f"Error in deployment operations: {e}")

        # Clean up
        cleanup_resources(datacrunch)

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Attempt cleanup even if there was an error
        try:
            cleanup_resources(datacrunch)
        except Exception as cleanup_error:
            print(f"Error during cleanup after failure: {cleanup_error}")


if __name__ == "__main__":
    main()
