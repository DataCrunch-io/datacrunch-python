"""
This example demonstrates how to manage environment variables for container deployments.
It shows how to:
1. Get environment variables for a deployment
2. Add new environment variables to a container
3. Update existing environment variables
4. Delete environment variables
"""

import os
from datacrunch.containers import EnvVar, EnvVarType
from datacrunch import DataCrunchClient
from typing import Dict, List

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Initialize DataCrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Example deployment and container names
DEPLOYMENT_NAME = "my-deployment"
CONTAINER_NAME = "main"


def print_env_vars(env_vars: Dict[str, List[EnvVar]]) -> None:
    """Helper function to print environment variables"""
    print("\nCurrent environment variables:")
    for container_name, vars in env_vars.items():
        print(f"\nContainer: {container_name}")
        for var in vars:
            print(f"  {var.name}: {var.value_or_reference_to_secret} ({var.type})")


def main():
    # First, let's get the current environment variables
    print("Getting current environment variables...")
    env_vars = datacrunch.containers.get_deployment_environment_variables(
        DEPLOYMENT_NAME)
    print_env_vars(env_vars)

    # Create a new secret
    secret_name = "my-secret-key"
    datacrunch.containers.create_secret(
        secret_name,
        "my-secret-value"
    )

    # Add new environment variables
    print("\nAdding new environment variables...")
    new_env_vars = [
        EnvVar(
            name="API_KEY",
            value_or_reference_to_secret=secret_name,
            type=EnvVarType.SECRET
        ),
        EnvVar(
            name="DEBUG",
            value_or_reference_to_secret="true",
            type=EnvVarType.PLAIN
        )
    ]

    env_vars = datacrunch.containers.add_deployment_environment_variables(
        deployment_name=DEPLOYMENT_NAME,
        container_name=CONTAINER_NAME,
        env_vars=new_env_vars
    )
    print_env_vars(env_vars)

    # Update existing environment variables
    print("\nUpdating environment variables...")
    updated_env_vars = [
        EnvVar(
            name="DEBUG",
            value_or_reference_to_secret="false",
            type=EnvVarType.PLAIN
        ),
    ]

    env_vars = datacrunch.containers.update_deployment_environment_variables(
        deployment_name=DEPLOYMENT_NAME,
        container_name=CONTAINER_NAME,
        env_vars=updated_env_vars
    )
    print_env_vars(env_vars)

    # Delete environment variables
    print("\nDeleting environment variables...")
    env_vars = datacrunch.containers.delete_deployment_environment_variables(
        deployment_name=DEPLOYMENT_NAME,
        container_name=CONTAINER_NAME,
        env_var_names=["DEBUG"]
    )
    print_env_vars(env_vars)


if __name__ == "__main__":
    main()
