"""Example script demonstrating SGLang model deployment using the DataCrunch API.

This script provides an example of deploying a SGLang server with deepseek-ai/deepseek-llm-7b-chat model,
including creation, monitoring, testing, and cleanup.
"""

import os
import time
import signal
import sys
import requests

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
    EntrypointOverridesSettings,
    EnvVar,
    EnvVarType,
    ContainerRegistrySettings,
    Deployment,
    ContainerDeploymentStatus,
)

# Configuration constants
DEPLOYMENT_NAME = "sglang-deployment-tutorial"
CONTAINER_NAME = "sglang-server"
MODEL_PATH = "deepseek-ai/deepseek-llm-7b-chat"
HF_SECRET_NAME = "huggingface-token"
IMAGE_URL = "docker.io/lmsysorg/sglang:v0.4.1.post6-cu124"
CONTAINERS_API_URL = f'https://containers.datacrunch.io/{DEPLOYMENT_NAME}'

# Get confidential values from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')
HF_TOKEN = os.environ.get('HF_TOKEN')
INFERENCE_API_KEY = os.environ.get('INFERENCE_API_KEY')

# DataCrunch client instance (global for graceful shutdown)
datacrunch = None


def wait_for_deployment_health(datacrunch_client: DataCrunchClient, deployment_name: str, max_attempts: int = 20, delay: int = 30) -> bool:
    """Wait for deployment to reach healthy status.

    Args:
        client: DataCrunch API client
        deployment_name: Name of the deployment to check
        max_attempts: Maximum number of status checks
        delay: Delay between checks in seconds

    Returns:
        bool: True if deployment is healthy, False otherwise
    """
    print(f"Waiting for deployment to be healthy (may take several minutes to download model)...")
    for attempt in range(max_attempts):
        try:
            status = datacrunch_client.containers.get_deployment_status(
                deployment_name)
            print(
                f"Attempt {attempt+1}/{max_attempts} - Deployment status: {status}")
            if status == ContainerDeploymentStatus.HEALTHY:
                return True
            time.sleep(delay)
        except APIException as e:
            print(f"Error checking deployment status: {e}")
            return False
    return False


def cleanup_resources(datacrunch_client: DataCrunchClient) -> None:
    """Clean up all created resources.

    Args:
        client: DataCrunchAPI client
    """
    try:
        # Delete deployment
        datacrunch_client.containers.delete_deployment(DEPLOYMENT_NAME)
        print("Deployment deleted")
    except APIException as e:
        print(f"Error during cleanup: {e}")


def graceful_shutdown(signum, frame) -> None:
    """Handle graceful shutdown on signals."""
    print(f"\nSignal {signum} received, cleaning up resources...")
    try:
        cleanup_resources(datacrunch)
    except Exception as e:
        print(f"Error during cleanup: {e}")
    sys.exit(0)


def test_deployment(base_url: str, api_key: str) -> None:
    """Test the deployment with a simple request.

    Args:
        base_url: The base URL of the deployment
        api_key: The API key for authentication
    """
    # First, check if the model info endpoint is working
    model_info_url = f"{base_url}/get_model_info"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        print("\nTesting /get_model_info endpoint...")
        response = requests.get(model_info_url, headers=headers)
        if response.status_code == 200:
            print("Model info endpoint is working!")
            print(f"Response: {response.json()}")
        else:
            print(f"Request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return

        # Now test completions endpoint
        print("\nTesting completions API with streaming...")
        completions_url = f"{base_url}/v1/completions"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }

        data = {
            "model": MODEL_PATH,
            "prompt": "Solar wind is a curious phenomenon. Tell me more about it",
            "max_tokens": 128,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": True
        }

        with requests.post(completions_url, headers=headers, json=data, stream=True) as response:
            if response.status_code == 200:
                print("Stream started. Receiving first 5 events...\n")
                for i, line in enumerate(response.iter_lines(decode_unicode=True)):
                    if line:
                        print(line)
                    if i >= 4:  # Only show first 5 events
                        print("...(response continues)...")
                        break
            else:
                print(
                    f"Request failed with status code {response.status_code}")
                print(f"Response: {response.text}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


def main() -> None:
    """Main function demonstrating SGLang deployment."""
    try:
        if not HF_TOKEN:
            print("Please set HF_TOKEN environment variable with your Hugging Face token")
            return

        # Initialize client
        global datacrunch
        datacrunch = DataCrunchClient(
            DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

        # Register signal handlers for cleanup
        signal.signal(signal.SIGINT, graceful_shutdown)
        signal.signal(signal.SIGTERM, graceful_shutdown)

        # Create a secret for the Hugging Face token
        print(f"Creating secret for Hugging Face token: {HF_SECRET_NAME}")
        try:
            # Check if secret already exists
            existing_secrets = datacrunch.containers.get_secrets()
            secret_exists = any(
                secret.name == HF_SECRET_NAME for secret in existing_secrets)

            if not secret_exists:
                datacrunch.containers.create_secret(
                    HF_SECRET_NAME, HF_TOKEN)
                print(f"Secret '{HF_SECRET_NAME}' created successfully")
            else:
                print(
                    f"Secret '{HF_SECRET_NAME}' already exists, using existing secret")
        except APIException as e:
            print(f"Error creating secret: {e}")
            return

        # Create container configuration
        container = Container(
            image=IMAGE_URL,
            exposed_port=30000,
            healthcheck=HealthcheckSettings(
                enabled=True,
                port=30000,
                path="/health"
            ),
            entrypoint_overrides=EntrypointOverridesSettings(
                enabled=True,
                cmd=["python3", "-m", "sglang.launch_server", "--model-path",
                     MODEL_PATH, "--host", "0.0.0.0", "--port", "30000"]
            ),
            env=[
                EnvVar(
                    name="HF_TOKEN",
                    value_or_reference_to_secret=HF_SECRET_NAME,
                    type=EnvVarType.SECRET
                )
            ]
        )

        # Create scaling configuration - default values
        scaling_options = ScalingOptions(
            min_replica_count=1,
            max_replica_count=2,
            scale_down_policy=ScalingPolicy(delay_seconds=300),
            scale_up_policy=ScalingPolicy(delay_seconds=300),
            queue_message_ttl_seconds=500,
            concurrent_requests_per_replica=1,
            scaling_triggers=ScalingTriggers(
                queue_load=QueueLoadScalingTrigger(threshold=1),
                cpu_utilization=UtilizationScalingTrigger(
                    enabled=True,
                    threshold=90
                ),
                gpu_utilization=UtilizationScalingTrigger(
                    enabled=True,
                    threshold=90
                )
            )
        )

        # Create registry and compute settings
        registry_settings = ContainerRegistrySettings(is_private=False)
        # For a 7B model, General Compute (24GB VRAM) is sufficient
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
        print("This will take several minutes while the model is downloaded and the server starts...")

        # Wait for deployment to be healthy
        if not wait_for_deployment_health(datacrunch, DEPLOYMENT_NAME):
            print("Deployment health check failed")
            cleanup_resources(datacrunch)
            return

        # Get the deployment endpoint URL and inference API key
        containers_api_url = CONTAINERS_API_URL
        inference_api_key = INFERENCE_API_KEY

        # If not provided as environment variables, prompt the user
        if not containers_api_url:
            containers_api_url = input(
                "Enter your Containers API URL from the DataCrunch dashboard: ")
        else:
            print(
                f"Using Containers API URL from environment: {containers_api_url}")

        if not inference_api_key:
            inference_api_key = input(
                "Enter your Inference API Key from the DataCrunch dashboard: ")
        else:
            print("Using Inference API Key from environment")

        # Test the deployment
        if containers_api_url and inference_api_key:
            print("\nTesting the deployment...")
            test_deployment(containers_api_url, inference_api_key)

        # Cleanup or keep running based on user input
        keep_running = input(
            "\nDo you want to keep the deployment running? (y/n): ")
        if keep_running.lower() != 'y':
            cleanup_resources(datacrunch)
        else:
            print(
                f"Deployment {DEPLOYMENT_NAME} is running. Don't forget to delete it when finished.")
            print("You can delete it from the DataCrunch dashboard or by running:")
            print(f"datacrunch.containers.delete('{DEPLOYMENT_NAME}')")

    except Exception as e:
        print(f"Unexpected error: {e}")
        # Attempt cleanup even if there was an error
        try:
            cleanup_resources(datacrunch)
        except Exception as cleanup_error:
            print(f"Error during cleanup after failure: {cleanup_error}")


if __name__ == "__main__":
    main()
