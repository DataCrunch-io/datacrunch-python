from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config, Undefined  # type: ignore
from typing import List, Optional, Dict
from datetime import datetime
from marshmallow import fields
from enum import Enum


# API endpoints
CONTAINER_DEPLOYMENTS_ENDPOINT = '/container-deployments'
SERVERLESS_COMPUTE_RESOURCES_ENDPOINT = '/serverless-compute-resources'
SECRETS_ENDPOINT = '/secrets'
CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT = '/container-registry-credentials'


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
    enabled: bool
    port: Optional[int] = None
    path: Optional[str] = None


@dataclass_json
@dataclass
class EntrypointOverridesSettings:
    enabled: bool
    entrypoint: Optional[List[str]] = None
    cmd: Optional[List[str]] = None


@dataclass_json
@dataclass
class EnvVar:
    name: str
    value_or_reference_to_secret: str
    type: EnvVarType  # "plain" or "secret"


@dataclass_json
@dataclass
class VolumeMount:
    type: VolumeMountType  # "scratch" or "secret"
    mount_path: str


@dataclass_json
@dataclass
class Container:
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
    name: str


@dataclass_json
@dataclass
class ContainerRegistrySettings:
    is_private: bool
    credentials: Optional[ContainerRegistryCredentials] = None


@dataclass_json
@dataclass
class ComputeResource:
    name: str
    size: int
    # Made optional since it's only used in API responses
    is_available: Optional[bool] = None


@dataclass_json
@dataclass
class ScalingPolicy:
    delay_seconds: int


@dataclass_json
@dataclass
class QueueLoadScalingTrigger:
    threshold: float


@dataclass_json
@dataclass
class UtilizationScalingTrigger:
    enabled: bool
    threshold: Optional[float] = None


@dataclass_json
@dataclass
class ScalingTriggers:
    queue_load: Optional[QueueLoadScalingTrigger] = None
    cpu_utilization: Optional[UtilizationScalingTrigger] = None
    gpu_utilization: Optional[UtilizationScalingTrigger] = None


@dataclass_json
@dataclass
class ScalingOptions:
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
    name: str
    container_registry_settings: ContainerRegistrySettings
    containers: List[Container]
    compute: ComputeResource
    is_spot: bool = False
    endpoint_base_url: Optional[str] = None
    scaling: Optional[ScalingOptions] = None
    created_at: Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=lambda x: x.isoformat() if x is not None else None,
            decoder=lambda x: datetime.fromisoformat(
                x) if x is not None else None,
            mm_field=fields.DateTime(format='iso')
        )
    )


@dataclass_json
@dataclass
class ReplicaInfo:
    id: str
    status: str
    started_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


@dataclass_json
@dataclass
class Secret:
    """A secret model class"""
    name: str
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


@dataclass_json
@dataclass
class RegistryCredential:
    """A container registry credential model class"""
    name: str
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


class ContainersService:
    """Service for managing container deployments"""

    def __init__(self, http_client) -> None:
        """Initialize the containers service

        :param http_client: HTTP client for making API requests
        :type http_client: Any
        """
        self.client = http_client

    def get(self) -> List[Deployment]:
        """Get all deployments

        :return: list of deployments
        :rtype: List[Deployment]
        """
        response = self.client.get(CONTAINER_DEPLOYMENTS_ENDPOINT)
        return [Deployment.from_dict(deployment, infer_missing=True) for deployment in response.json()]

    def get_by_name(self, deployment_name: str) -> Deployment:
        """Get a deployment by name

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: deployment
        :rtype: Deployment
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}")
        return Deployment.from_dict(response.json(), infer_missing=True)

    def create(
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

    def update(self, deployment_name: str, deployment: Deployment) -> Deployment:
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

    def delete(self, deployment_name: str) -> None:
        """Delete a deployment

        :param deployment_name: name of the deployment to delete
        :type deployment_name: str
        """
        self.client.delete(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}")

    def get_status(self, deployment_name: str) -> ContainerDeploymentStatus:
        """Get deployment status

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: deployment status
        :rtype: ContainerDeploymentStatus
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/status")
        return ContainerDeploymentStatus(response.json()["status"])

    def restart(self, deployment_name: str) -> None:
        """Restart a deployment

        :param deployment_name: name of the deployment to restart
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/restart")

    def get_scaling_options(self, deployment_name: str) -> Dict:
        """Get deployment scaling options

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: scaling options
        :rtype: Dict
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/scaling")
        return response.json()

    def update_scaling_options(self, deployment_name: str, scaling_options: Dict) -> Dict:
        """Update deployment scaling options

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param scaling_options: new scaling options
        :type scaling_options: Dict
        :return: updated scaling options
        :rtype: Dict
        """
        response = self.client.patch(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/scaling",
            scaling_options
        )
        return response.json()

    def get_replicas(self, deployment_name: str) -> Dict:
        """Get deployment replicas

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: replicas information
        :rtype: Dict
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/replicas")
        return response.json()

    def purge_queue(self, deployment_name: str) -> None:
        """Purge deployment queue

        :param deployment_name: name of the deployment
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/purge-queue")

    def pause(self, deployment_name: str) -> None:
        """Pause a deployment

        :param deployment_name: name of the deployment to pause
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/pause")

    def resume(self, deployment_name: str) -> None:
        """Resume a deployment

        :param deployment_name: name of the deployment to resume
        :type deployment_name: str
        """
        self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/resume")

    def get_environment_variables(self, deployment_name: str) -> Dict:
        """Get deployment environment variables

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: environment variables
        :rtype: Dict
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables")
        return response.json()

    def add_environment_variables(self, deployment_name: str, container_name: str, env_vars: List[Dict]) -> Dict:
        """Add environment variables to a container

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param container_name: name of the container
        :type container_name: str
        :param env_vars: environment variables to add
        :type env_vars: List[Dict]
        :return: updated environment variables
        :rtype: Dict
        """
        response = self.client.post(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables",
            {"container_name": container_name, "env": env_vars}
        )
        return response.json()

    def update_environment_variables(self, deployment_name: str, container_name: str, env_vars: List[Dict]) -> Dict:
        """Update environment variables of a container

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param container_name: name of the container
        :type container_name: str
        :param env_vars: updated environment variables
        :type env_vars: List[Dict]
        :return: updated environment variables
        :rtype: Dict
        """
        response = self.client.patch(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables",
            {"container_name": container_name, "env": env_vars}
        )
        return response.json()

    def delete_environment_variables(self, deployment_name: str, container_name: str, env_var_names: List[str]) -> Dict:
        """Delete environment variables from a container

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :param container_name: name of the container
        :type container_name: str
        :param env_var_names: names of environment variables to delete
        :type env_var_names: List[str]
        :return: remaining environment variables
        :rtype: Dict
        """
        response = self.client.delete(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables",
            {"container_name": container_name, "env": env_var_names}
        )
        return response.json()

    def get_compute_resources(self) -> List[ComputeResource]:
        """Get available compute resources

        :return: list of compute resources
        :rtype: List[ComputeResource]
        """
        response = self.client.get(SERVERLESS_COMPUTE_RESOURCES_ENDPOINT)
        return [ComputeResource.from_dict(resource) for resource in response.json()]

    def get_secrets(self) -> List[Secret]:
        """Get all secrets

        :return: list of secrets
        :rtype: List[Secret]
        """
        response = self.client.get(SECRETS_ENDPOINT)
        return [Secret.from_dict(secret) for secret in response.json()]

    def create_secret(self, name: str, value: str) -> Secret:
        """Create a new secret

        :param name: name of the secret
        :type name: str
        :param value: value of the secret
        :type value: str
        :return: created secret
        :rtype: Secret
        """
        response = self.client.post(
            SECRETS_ENDPOINT, {"name": name, "value": value})
        return Secret.from_dict(response.json())

    def delete_secret(self, secret_name: str, force: bool = False) -> None:
        """Delete a secret

        :param secret_name: name of the secret to delete
        :type secret_name: str
        :param force: force delete even if secret is in use
        :type force: bool
        """
        self.client.delete(
            f"{SECRETS_ENDPOINT}/{secret_name}", params={"force": force})

    def get_registry_credentials(self) -> List[RegistryCredential]:
        """Get all registry credentials

        :return: list of registry credentials
        :rtype: List[RegistryCredential]
        """
        response = self.client.get(CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT)
        return [RegistryCredential.from_dict(credential) for credential in response.json()]

    def add_registry_credentials(self, name: str, registry_type: ContainerRegistryType, username: str, access_token: str) -> RegistryCredential:
        """Add registry credentials

        :param name: name of the credentials
        :type name: str
        :param registry_type: type of registry (e.g. ContainerRegistryType.DOCKERHUB)
        :type registry_type: ContainerRegistryType
        :param username: registry username
        :type username: str
        :param access_token: registry access token
        :type access_token: str
        :return: created registry credential
        :rtype: RegistryCredential
        """
        data = {
            "name": name,
            "registry_type": registry_type.value,
            "username": username,
            "access_token": access_token
        }
        response = self.client.post(
            CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT, data)
        return RegistryCredential.from_dict(response.json())

    def delete_registry_credentials(self, credentials_name: str) -> None:
        """Delete registry credentials

        :param credentials_name: name of the credentials to delete
        :type credentials_name: str
        """
        self.client.delete(
            f"{CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT}/{credentials_name}")
