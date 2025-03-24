from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined  # type: ignore
from typing import List, Optional, Dict
from enum import Enum


# API endpoints
CONTAINER_DEPLOYMENTS_ENDPOINT = '/container-deployments'
SERVERLESS_COMPUTE_RESOURCES_ENDPOINT = '/serverless-compute-resources'
CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT = '/container-registry-credentials'
SECRETS_ENDPOINT = '/secrets'


class EnvVarType(str, Enum):
    PLAIN = "plain"
    SECRET = "secret"


class VolumeMountType(str, Enum):
    SCRATCH = "scratch"
    SECRET = "secret"


class ContainerRegistryType(str, Enum):
    GCR = "gcr"
    DOCKERHUB = "dockerhub"
    GITHUB = "ghcr"
    AWS_ECR = "aws-ecr"
    CUSTOM = "custom"


class ContainerDeploymentStatus(str, Enum):
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    PAUSED = "paused"
    QUOTA_REACHED = "quota_reached"
    IMAGE_PULLING = "image_pulling"
    VERSION_UPDATING = "version_updating"


@dataclass_json
@dataclass
class HealthcheckSettings:
    """Settings for container health checking.

    :param enabled: Whether health checking is enabled
    :param port: Port number to perform health check on
    :param path: HTTP path to perform health check on
    """
    enabled: bool = True
    port: Optional[int] = None
    path: Optional[str] = None


@dataclass_json
@dataclass
class EntrypointOverridesSettings:
    """Settings for overriding container entrypoint and command.

    :param enabled: Whether entrypoint overrides are enabled
    :param entrypoint: List of strings forming the entrypoint command
    :param cmd: List of strings forming the command arguments
    """
    enabled: bool = True
    entrypoint: Optional[List[str]] = None
    cmd: Optional[List[str]] = None


@dataclass_json
@dataclass
class EnvVar:
    """Environment variable configuration for containers.

    :param name: Name of the environment variable
    :param value_or_reference_to_secret: Direct value or reference to a secret
    :param type: Type of the environment variable
    """
    name: str
    value_or_reference_to_secret: str
    type: EnvVarType


@dataclass_json
@dataclass
class VolumeMount:
    """Volume mount configuration for containers.

    :param type: Type of volume mount
    :param mount_path: Path where the volume should be mounted in the container
    """
    type: VolumeMountType
    mount_path: str


@dataclass_json
@dataclass
class Container:
    """Container configuration for deployments.

    :param name: Name of the container
    :param image: Container image to use
    :param exposed_port: Port to expose from the container
    :param healthcheck: Optional health check configuration
    :param entrypoint_overrides: Optional entrypoint override settings
    :param env: Optional list of environment variables
    :param volume_mounts: Optional list of volume mounts
    """
    name: str
    image: str
    exposed_port: int
    healthcheck: Optional[HealthcheckSettings] = None
    entrypoint_overrides: Optional[EntrypointOverridesSettings] = None
    env: Optional[List[EnvVar]] = None
    volume_mounts: Optional[List[VolumeMount]] = None


@dataclass_json
@dataclass
class ContainerRegistryCredentials:
    """Credentials for accessing a container registry.

    :param name: Name of the credentials
    """
    name: str


@dataclass_json
@dataclass
class ContainerRegistrySettings:
    """Settings for container registry access.

    :param is_private: Whether the registry is private
    :param credentials: Optional credentials for accessing private registry
    """
    is_private: bool
    credentials: Optional[ContainerRegistryCredentials] = None


@dataclass_json
@dataclass
class ComputeResource:
    """Compute resource configuration.

    :param name: Name of the compute resource
    :param size: Size of the compute resource
    :param is_available: Whether the compute resource is currently available
    """
    name: str
    size: int
    # Made optional since it's only used in API responses
    is_available: Optional[bool] = None


@dataclass_json
@dataclass
class ScalingPolicy:
    """Policy for controlling scaling behavior.

    :param delay_seconds: Number of seconds to wait before applying scaling action
    """
    delay_seconds: int


@dataclass_json
@dataclass
class QueueLoadScalingTrigger:
    """Trigger for scaling based on queue load.

    :param threshold: Queue load threshold that triggers scaling
    """
    threshold: float


@dataclass_json
@dataclass
class UtilizationScalingTrigger:
    """Trigger for scaling based on resource utilization.

    :param enabled: Whether this trigger is enabled
    :param threshold: Utilization threshold that triggers scaling
    """
    enabled: bool
    threshold: Optional[float] = None


@dataclass_json
@dataclass
class ScalingTriggers:
    """Collection of triggers that can cause scaling actions.

    :param queue_load: Optional trigger based on queue load
    :param cpu_utilization: Optional trigger based on CPU utilization
    :param gpu_utilization: Optional trigger based on GPU utilization
    """
    queue_load: Optional[QueueLoadScalingTrigger] = None
    cpu_utilization: Optional[UtilizationScalingTrigger] = None
    gpu_utilization: Optional[UtilizationScalingTrigger] = None


@dataclass_json
@dataclass
class ScalingOptions:
    """Configuration for automatic scaling behavior.

    :param min_replica_count: Minimum number of replicas to maintain
    :param max_replica_count: Maximum number of replicas allowed
    :param scale_down_policy: Policy for scaling down replicas
    :param scale_up_policy: Policy for scaling up replicas
    :param queue_message_ttl_seconds: Time-to-live for queue messages in seconds
    :param concurrent_requests_per_replica: Number of concurrent requests each replica can handle
    :param scaling_triggers: Configuration for various scaling triggers
    """
    min_replica_count: int
    max_replica_count: int
    scale_down_policy: ScalingPolicy
    scale_up_policy: ScalingPolicy
    queue_message_ttl_seconds: int
    concurrent_requests_per_replica: int
    scaling_triggers: ScalingTriggers


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Deployment:
    """Configuration for a container deployment.

    :param name: Name of the deployment
    :param container_registry_settings: Settings for accessing container registry
    :param containers: List of containers in the deployment
    :param compute: Compute resource configuration
    :param is_spot: Whether is spot deployment
    :param endpoint_base_url: Optional base URL for the deployment endpoint
    :param scaling: Optional scaling configuration
    :param created_at: Timestamp when the deployment was created
    """
    name: str
    container_registry_settings: ContainerRegistrySettings
    containers: List[Container]
    compute: ComputeResource
    is_spot: bool = False
    endpoint_base_url: Optional[str] = None
    scaling: Optional[ScalingOptions] = None
    created_at: Optional[str] = None


@dataclass_json
@dataclass
class ReplicaInfo:
    """Information about a deployment replica.

    :param id: Unique identifier of the replica
    :param status: Current status of the replica
    :param started_at: Timestamp when the replica was started
    """
    id: str
    status: str
    started_at: str


@dataclass_json
@dataclass
class Secret:
    """A secret model class"""
    name: str
    created_at: str


@dataclass_json
@dataclass
class RegistryCredential:
    """A container registry credential model class"""
    name: str
    created_at: str


@dataclass_json
@dataclass
class BaseRegistryCredentials:
    """Base class for registry credentials"""
    name: str
    type: ContainerRegistryType


@dataclass_json
@dataclass
class DockerHubCredentials(BaseRegistryCredentials):
    """Credentials for DockerHub registry"""
    username: str
    access_token: str

    def __init__(self, name: str, username: str, access_token: str):
        super().__init__(name=name, type=ContainerRegistryType.DOCKERHUB)
        self.username = username
        self.access_token = access_token


@dataclass_json
@dataclass
class GithubCredentials(BaseRegistryCredentials):
    """Credentials for GitHub Container Registry"""
    username: str
    access_token: str

    def __init__(self, name: str, username: str, access_token: str):
        super().__init__(name=name, type=ContainerRegistryType.GITHUB)
        self.username = username
        self.access_token = access_token


@dataclass_json
@dataclass
class GCRCredentials(BaseRegistryCredentials):
    """Credentials for Google Container Registry"""
    service_account_key: str

    def __init__(self, name: str, service_account_key: str):
        super().__init__(name=name, type=ContainerRegistryType.GCR)
        self.service_account_key = service_account_key


@dataclass_json
@dataclass
class AWSECRCredentials(BaseRegistryCredentials):
    """Credentials for AWS Elastic Container Registry"""
    access_key_id: str
    secret_access_key: str
    region: str
    ecr_repo: str

    def __init__(self, name: str, access_key_id: str, secret_access_key: str, region: str, ecr_repo: str):
        super().__init__(name=name, type=ContainerRegistryType.AWS_ECR)
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self.ecr_repo = ecr_repo


@dataclass_json
@dataclass
class CustomRegistryCredentials(BaseRegistryCredentials):
    """Credentials for custom container registries"""
    docker_config_json: str

    def __init__(self, name: str, docker_config_json: str):
        super().__init__(name=name, type=ContainerRegistryType.CUSTOM)
        self.docker_config_json = docker_config_json


class ContainersService:
    """Service for managing container deployments"""

    def __init__(self, http_client) -> None:
        """Initialize the containers service

        :param http_client: HTTP client for making API requests
        :type http_client: Any
        """
        self.client = http_client

    def get_deployments(self) -> List[Deployment]:
        """Get all deployments

        :return: list of deployments
        :rtype: List[Deployment]
        """
        response = self.client.get(CONTAINER_DEPLOYMENTS_ENDPOINT)
        return [Deployment.from_dict(deployment, infer_missing=True) for deployment in response.json()]

    def get_deployment_by_name(self, deployment_name: str) -> Deployment:
        """Get a deployment by name

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: deployment
        :rtype: Deployment
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}")
        return Deployment.from_dict(response.json(), infer_missing=True)

    def create_deployment(
        self,
        deployment: Deployment
    ) -> Deployment:
        """Create a new deployment

        :param deployment: deployment configuration
        :type deployment: Deployment
        :return: created deployment
        :rtype: Deployment
        """
        response = self.client.post(
            CONTAINER_DEPLOYMENTS_ENDPOINT,
            deployment.to_dict()
        )
        return Deployment.from_dict(response.json(), infer_missing=True)

    def update_deployment(self, deployment_name: str, deployment: Deployment) -> Deployment:
        """Update an existing deployment

        :param deployment_name: name of the deployment to update
        :type deployment_name: str
        :param deployment: updated deployment
        :type deployment: Deployment
        :return: updated deployment
        :rtype: Deployment
        """
        response = self.client.patch(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}",
            deployment.to_dict()
        )
        return Deployment.from_dict(response.json(), infer_missing=True)

    def delete_deployment(self, deployment_name: str) -> None:
        """Delete a deployment

        :param deployment_name: name of the deployment to delete
        :type deployment_name: str
        """
        self.client.delete(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}")

    def get_deployment_status(self, deployment_name: str) -> ContainerDeploymentStatus:
        """Get deployment status

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: deployment status
        :rtype: ContainerDeploymentStatus
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/status")
        return ContainerDeploymentStatus(response.json()["status"])

    def restart_deployment(self, deployment_name: str) -> None:
        """Restart a deployment

        :param deployment_name: name of the deployment to restart
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/restart")

    def get_deployment_scaling_options(self, deployment_name: str) -> ScalingOptions:
        """Get deployment scaling options

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: scaling options
        :rtype: ScalingOptions
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/scaling")
        return ScalingOptions.from_dict(response.json())

    def update_deployment_scaling_options(self, deployment_name: str, scaling_options: ScalingOptions) -> ScalingOptions:
        """Update deployment scaling options

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param scaling_options: new scaling options
        :type scaling_options: ScalingOptions
        :return: updated scaling options
        :rtype: ScalingOptions
        """
        response = self.client.patch(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/scaling",
            scaling_options.to_dict()
        )
        return ScalingOptions.from_dict(response.json())

    def get_deployment_replicas(self, deployment_name: str) -> List[ReplicaInfo]:
        """Get deployment replicas

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: list of replicas information
        :rtype: List[ReplicaInfo]
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/replicas")
        return [ReplicaInfo.from_dict(replica) for replica in response.json()["list"]]

    def purge_deployment_queue(self, deployment_name: str) -> None:
        """Purge deployment queue

        :param deployment_name: name of the deployment
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/purge-queue")

    def pause_deployment(self, deployment_name: str) -> None:
        """Pause a deployment

        :param deployment_name: name of the deployment to pause
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/pause")

    def resume_deployment(self, deployment_name: str) -> None:
        """Resume a deployment

        :param deployment_name: name of the deployment to resume
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/resume")

    def get_deployment_environment_variables(self, deployment_name: str) -> Dict[str, List[EnvVar]]:
        """Get deployment environment variables

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: dictionary mapping container names to their environment variables
        :rtype: Dict[str, List[EnvVar]]
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables")
        result = {}
        for item in response.json():
            container_name = item["container_name"]
            env_vars = item["env"]
            result[container_name] = [EnvVar.from_dict(
                env_var) for env_var in env_vars]
        return result

    def add_deployment_environment_variables(self, deployment_name: str, container_name: str, env_vars: List[EnvVar]) -> Dict[str, List[EnvVar]]:
        """Add environment variables to a container

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param container_name: name of the container
        :type container_name: str
        :param env_vars: environment variables to add
        :type env_vars: List[EnvVar]
        :return: updated environment variables
        :rtype: Dict[str, List[EnvVar]]
        """
        response = self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables",
            {"container_name": container_name, "env": [
                env_var.to_dict() for env_var in env_vars]}
        )
        result = {}
        for item in response.json():
            container_name = item["container_name"]
            env_vars = item["env"]
            result[container_name] = [EnvVar.from_dict(
                env_var) for env_var in env_vars]
        return result

    def update_deployment_environment_variables(self, deployment_name: str, container_name: str, env_vars: List[EnvVar]) -> Dict[str, List[EnvVar]]:
        """Update environment variables of a container

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param container_name: name of the container
        :type container_name: str
        :param env_vars: updated environment variables
        :type env_vars: List[EnvVar]
        :return: updated environment variables
        :rtype: Dict[str, List[EnvVar]] 
        """
        response = self.client.patch(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables",
            {"container_name": container_name, "env": [
                env_var.to_dict() for env_var in env_vars]}
        )
        result = {}
        item = response.json()
        container_name = item["container_name"]
        env_vars = item["env"]
        result[container_name] = [EnvVar.from_dict(
            env_var) for env_var in env_vars]
        return result

    def delete_deployment_environment_variables(self, deployment_name: str, container_name: str, env_var_names: List[str]) -> Dict[str, List[EnvVar]]:
        """Delete environment variables from a container

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param container_name: name of the container
        :type container_name: str
        :param env_var_names: names of environment variables to delete
        :type env_var_names: List[str]
        :return: remaining environment variables
        :rtype: Dict[str, List[EnvVar]]
        """
        response = self.client.delete(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables",
            {"container_name": container_name, "env": env_var_names}
        )
        result = {}
        for item in response.json():
            container_name = item["container_name"]
            env_vars = item["env"]
            result[container_name] = [EnvVar.from_dict(
                env_var) for env_var in env_vars]
        return result

    def get_compute_resources(self) -> List[ComputeResource]:
        """Get available compute resources

        :return: list of compute resources
        :rtype: List[ComputeResource]
        """
        response = self.client.get(SERVERLESS_COMPUTE_RESOURCES_ENDPOINT)
        resources = []
        for resource_group in response.json():
            for resource in resource_group:
                resources.append(ComputeResource.from_dict(resource))
        return resources

    def get_secrets(self) -> List[Secret]:
        """Get all secrets

        :return: list of secrets
        :rtype: List[Secret]
        """
        response = self.client.get(SECRETS_ENDPOINT)
        return [Secret.from_dict(secret) for secret in response.json()]

    def create_secret(self, name: str, value: str) -> None:
        """Create a new secret

        :param name: name of the secret
        :type name: str
        :param value: value of the secret
        :type value: str
        """
        self.client.post(SECRETS_ENDPOINT, {"name": name, "value": value})

    def delete_secret(self, secret_name: str, force: bool = False) -> None:
        """Delete a secret

        :param secret_name: name of the secret to delete
        :type secret_name: str
        :param force: force delete even if secret is in use
        :type force: bool
        """
        self.client.delete(
            f"{SECRETS_ENDPOINT}/{secret_name}", params={"force": str(force).lower()})

    def get_registry_credentials(self) -> List[RegistryCredential]:
        """Get all registry credentials

        :return: list of registry credentials
        :rtype: List[RegistryCredential]
        """
        response = self.client.get(CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT)
        return [RegistryCredential.from_dict(credential) for credential in response.json()]

    def add_registry_credentials(self, credentials: BaseRegistryCredentials) -> None:
        """Add registry credentials

        :param credentials: Registry credentials object
        :type credentials: BaseRegistryCredentials
        """
        data = credentials.to_dict()
        self.client.post(CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT, data)

    def delete_registry_credentials(self, credentials_name: str) -> None:
        """Delete registry credentials

        :param credentials_name: name of the credentials to delete
        :type credentials_name: str
        """
        self.client.delete(
            f"{CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT}/{credentials_name}")
