from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config, Undefined  # type: ignore
from typing import List, Optional, Dict
from datetime import datetime
from marshmallow import fields
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
    type: EnvVarType


@dataclass_json
@dataclass
class VolumeMount:
    type: VolumeMountType
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

    def get_deployment_replicas(self, deployment_name: str) -> Dict:
        """Get deployment replicas

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: replicas information
        :rtype: Dict
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/replicas")
        return response.json()

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

    def get_deployment_environment_variables(self, deployment_name: str) -> Dict:
        """Get deployment environment variables

        :param deployment_name: name of the deployment
        :type deployment_name: str
        :return: environment variables
        :rtype: Dict
        """
        response = self.client.get(
            f"{CONTAINER_DEPLOYMENTS_ENDPOINT}/{deployment_name}/environment-variables")
        return response.json()

    def add_deployment_environment_variables(self, deployment_name: str, container_name: str, env_vars: List[Dict]) -> Dict:
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

    def update_deployment_environment_variables(self, deployment_name: str, container_name: str, env_vars: List[Dict]) -> Dict:
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

    def delete_deployment_environment_variables(self, deployment_name: str, container_name: str, env_var_names: List[str]) -> Dict:
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
            f"{SECRETS_ENDPOINT}/{secret_name}", params={"force": str(force).lower()})

    def get_registry_credentials(self) -> List[RegistryCredential]:
        """Get all registry credentials

        :return: list of registry credentials
        :rtype: List[RegistryCredential]
        """
        response = self.client.get(CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT)
        return [RegistryCredential.from_dict(credential) for credential in response.json()]

    def add_registry_credentials(
        self,
        name: str,
        registry_type: ContainerRegistryType,
        username: str = None,
        access_token: str = None,
        service_account_key: str = None,
        docker_config_json: str = None,
        access_key_id: str = None,
        secret_access_key: str = None,
        region: str = None,
        ecr_repo: str = None
    ) -> None:
        """Add registry credentials

        :param name: name of the credentials
        :type name: str
        :param registry_type: type of registry (e.g. ContainerRegistryType.DOCKERHUB)
        :type registry_type: ContainerRegistryType
        :param username: registry username (required for DOCKERHUB and GITHUB)
        :type username: str
        :param access_token: registry access token (required for DOCKERHUB and GITHUB)
        :type access_token: str
        :param service_account_key: service account key JSON string (required for GCR)
        :type service_account_key: str
        :param docker_config_json: docker config JSON string (required for CUSTOM)
        :type docker_config_json: str
        :param access_key_id: AWS access key ID (required for AWS_ECR)
        :type access_key_id: str
        :param secret_access_key: AWS secret access key (required for AWS_ECR)
        :type secret_access_key: str
        :param region: AWS region (required for AWS_ECR)
        :type region: str
        :param ecr_repo: ECR repository URL (required for AWS_ECR)
        :type ecr_repo: str
        """
        data = {
            "name": name,
            "type": registry_type.value
        }

        # Add specific parameters based on registry type
        if registry_type == ContainerRegistryType.DOCKERHUB or registry_type == ContainerRegistryType.GITHUB:
            if not username or not access_token:
                raise ValueError(
                    f"Username and access_token are required for {registry_type.value} registry type")
            data["username"] = username
            data["access_token"] = access_token
        elif registry_type == ContainerRegistryType.GCR:
            if not service_account_key:
                raise ValueError(
                    "service_account_key is required for GCR registry type")
            data["service_account_key"] = service_account_key
        elif registry_type == ContainerRegistryType.AWS_ECR:
            if not all([access_key_id, secret_access_key, region, ecr_repo]):
                raise ValueError(
                    "access_key_id, secret_access_key, region, and ecr_repo are required for AWS_ECR registry type")
            data["access_key_id"] = access_key_id
            data["secret_access_key"] = secret_access_key
            data["region"] = region
            data["ecr_repo"] = ecr_repo
        elif registry_type == ContainerRegistryType.CUSTOM:
            if not docker_config_json:
                raise ValueError(
                    "docker_config_json is required for CUSTOM registry type")
            data["docker_config_json"] = docker_config_json

        self.client.post(CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT, data)

    def delete_registry_credentials(self, credentials_name: str) -> None:
        """Delete registry credentials

        :param credentials_name: name of the credentials to delete
        :type credentials_name: str
        """
        self.client.delete(
            f"{CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT}/{credentials_name}")
