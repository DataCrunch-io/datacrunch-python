import pytest
import responses  # https://github.com/getsentry/responses

from datacrunch.containers.containers import (
    CONTAINER_DEPLOYMENTS_ENDPOINT,
    CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT,
    SECRETS_ENDPOINT,
    SERVERLESS_COMPUTE_RESOURCES_ENDPOINT,
    Container,
    ContainerDeploymentStatus,
    ContainerRegistrySettings,
    ContainerRegistryType,
    ContainersService,
    Deployment,
    EnvVar,
    EnvVarType,
    EntrypointOverridesSettings,
    HealthcheckSettings,
    RegistryCredential,
    Secret,
    VolumeMount,
    VolumeMountType,
    ComputeResource,
    ScalingOptions,
    ScalingPolicy,
    ScalingTriggers,
    QueueLoadScalingTrigger,
    UtilizationScalingTrigger,
)
from datacrunch.exceptions import APIException

DEPLOYMENT_NAME = "test-deployment"
CONTAINER_NAME = "test-container"
COMPUTE_RESOURCE_NAME = "test-compute"
SECRET_NAME = "test-secret"
SECRET_VALUE = "test-secret-value"
REGISTRY_CREDENTIAL_NAME = "test-credential"
ENV_VAR_NAME = "TEST_VAR"
ENV_VAR_VALUE = "test-value"

INVALID_REQUEST = "INVALID_REQUEST"
INVALID_REQUEST_MESSAGE = "Invalid request"

# Sample deployment data for testing
DEPLOYMENT_DATA = {
    "name": DEPLOYMENT_NAME,
    "container_registry_settings": {
        "is_private": False
    },
    "containers": [
        {
            "name": CONTAINER_NAME,
            "image": "nginx:latest",
            "exposed_port": 80,
            "healthcheck": {
                "enabled": True,
                "port": 80,
                "path": "/health"
            },
            "entrypoint_overrides": {
                "enabled": False
            },
            "env": [
                {
                    "name": "ENV_VAR1",
                    "value_or_reference_to_secret": "value1",
                    "type": "plain"
                }
            ],
            "volume_mounts": [
                {
                    "type": "scratch",
                    "mount_path": "/data"
                }
            ]
        }
    ],
    "compute": {
        "name": COMPUTE_RESOURCE_NAME,
        "size": 1,
        "is_available": True
    },
    "is_spot": False,
    "endpoint_base_url": "https://test-deployment.datacrunch.io",
    "scaling": {
        "min_replica_count": 1,
        "max_replica_count": 3,
        "scale_down_policy": {
            "delay_seconds": 300
        },
        "scale_up_policy": {
            "delay_seconds": 60
        },
        "queue_message_ttl_seconds": 3600,
        "concurrent_requests_per_replica": 10,
        "scaling_triggers": {
            "queue_load": {
                "threshold": 0.75
            },
            "cpu_utilization": {
                "enabled": True,
                "threshold": 0.8
            },
            "gpu_utilization": {
                "enabled": False
            }
        }
    },
    "created_at": "2023-01-01T00:00:00+00:00"
}

# Sample compute resources data
COMPUTE_RESOURCES_DATA = [
    {
        "name": COMPUTE_RESOURCE_NAME,
        "size": 1,
        "is_available": True
    },
    {
        "name": "large-compute",
        "size": 4,
        "is_available": True
    }
]

# Sample secrets data
SECRETS_DATA = [
    {
        "name": SECRET_NAME,
        "created_at": "2023-01-01T00:00:00+00:00"
    }
]

# Sample registry credentials data
REGISTRY_CREDENTIALS_DATA = [
    {
        "name": REGISTRY_CREDENTIAL_NAME,
        "created_at": "2023-01-01T00:00:00+00:00"
    }
]

# Sample deployment status data
DEPLOYMENT_STATUS_DATA = {
    "status": "healthy"
}

# Sample replicas data
REPLICAS_DATA = {
    "replicas": [
        {
            "id": "replica-1",
            "status": "running",
            "started_at": "2023-01-01T00:00:00+00:00"
        }
    ]
}

# Sample environment variables data
ENV_VARS_DATA = {
    "container_name": CONTAINER_NAME,
    "env": [
        {
            "name": "ENV_VAR1",
            "value_or_reference_to_secret": "value1",
            "type": "plain"
        }
    ]
}


class TestContainersService:
    @pytest.fixture
    def containers_service(self, http_client):
        return ContainersService(http_client)

    @pytest.fixture
    def deployments_endpoint(self, http_client):
        return http_client._base_url + CONTAINER_DEPLOYMENTS_ENDPOINT

    @pytest.fixture
    def compute_resources_endpoint(self, http_client):
        return http_client._base_url + SERVERLESS_COMPUTE_RESOURCES_ENDPOINT

    @pytest.fixture
    def secrets_endpoint(self, http_client):
        return http_client._base_url + SECRETS_ENDPOINT

    @pytest.fixture
    def registry_credentials_endpoint(self, http_client):
        return http_client._base_url + CONTAINER_REGISTRY_CREDENTIALS_ENDPOINT

    @responses.activate
    def test_get_deployments(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            deployments_endpoint,
            json=[DEPLOYMENT_DATA],
            status=200
        )

        # act
        deployments = containers_service.get()
        deployment = deployments[0]

        # assert
        assert type(deployments) == list
        assert len(deployments) == 1
        assert type(deployment) == Deployment
        assert deployment.name == DEPLOYMENT_NAME
        assert len(deployment.containers) == 1
        assert type(deployment.containers[0]) == Container
        assert type(deployment.compute) == ComputeResource
        assert deployment.compute.name == COMPUTE_RESOURCE_NAME
        assert responses.assert_call_count(deployments_endpoint, 1) is True

    @responses.activate
    def test_get_deployment_by_name(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}"
        responses.add(
            responses.GET,
            url,
            json=DEPLOYMENT_DATA,
            status=200
        )

        # act
        deployment = containers_service.get_by_name(DEPLOYMENT_NAME)

        # assert
        assert type(deployment) == Deployment
        assert deployment.name == DEPLOYMENT_NAME
        assert len(deployment.containers) == 1
        assert deployment.containers[0].name == CONTAINER_NAME
        assert deployment.compute.name == COMPUTE_RESOURCE_NAME
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_get_deployment_by_name_error(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/nonexistent"
        responses.add(
            responses.GET,
            url,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            containers_service.get_by_name("nonexistent")

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_create_deployment(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            deployments_endpoint,
            json=DEPLOYMENT_DATA,
            status=200
        )

        # create deployment object
        container = Container(
            name=CONTAINER_NAME,
            image="nginx:latest",
            exposed_port=80,
            healthcheck=HealthcheckSettings(
                enabled=True, port=80, path="/health"),
            entrypoint_overrides=EntrypointOverridesSettings(enabled=False),
            env=[EnvVar(
                name="ENV_VAR1", value_or_reference_to_secret="value1", type=EnvVarType.PLAIN)],
            volume_mounts=[VolumeMount(
                type=VolumeMountType.SCRATCH, mount_path="/data")]
        )

        compute = ComputeResource(name=COMPUTE_RESOURCE_NAME, size=1)

        container_registry_settings = ContainerRegistrySettings(
            is_private=False)

        deployment = Deployment(
            name=DEPLOYMENT_NAME,
            container_registry_settings=container_registry_settings,
            containers=[container],
            compute=compute,
            is_spot=False
        )

        # act
        created_deployment = containers_service.create(deployment)

        # assert
        assert type(created_deployment) == Deployment
        assert created_deployment.name == DEPLOYMENT_NAME
        assert len(created_deployment.containers) == 1
        assert created_deployment.containers[0].name == CONTAINER_NAME
        assert created_deployment.compute.name == COMPUTE_RESOURCE_NAME
        assert responses.assert_call_count(deployments_endpoint, 1) is True

    @responses.activate
    def test_update_deployment(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}"
        responses.add(
            responses.PATCH,
            url,
            json=DEPLOYMENT_DATA,
            status=200
        )

        # create deployment object
        container = Container(
            name=CONTAINER_NAME,
            image="nginx:latest",
            exposed_port=80
        )

        container_registry_settings = ContainerRegistrySettings(
            is_private=False)

        compute = ComputeResource(name=COMPUTE_RESOURCE_NAME, size=1)

        deployment = Deployment(
            name=DEPLOYMENT_NAME,
            container_registry_settings=container_registry_settings,
            containers=[container],
            compute=compute
        )

        # act
        updated_deployment = containers_service.update(
            DEPLOYMENT_NAME, deployment)

        # assert
        assert type(updated_deployment) == Deployment
        assert updated_deployment.name == DEPLOYMENT_NAME
        assert len(updated_deployment.containers) == 1
        assert updated_deployment.containers[0].name == CONTAINER_NAME
        assert updated_deployment.compute.name == COMPUTE_RESOURCE_NAME
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_delete_deployment(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}"
        responses.add(
            responses.DELETE,
            url,
            status=204
        )

        # act
        containers_service.delete(DEPLOYMENT_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_get_deployment_status(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/status"
        responses.add(
            responses.GET,
            url,
            json=DEPLOYMENT_STATUS_DATA,
            status=200
        )

        # act
        status = containers_service.get_status(DEPLOYMENT_NAME)

        # assert
        assert status == ContainerDeploymentStatus.HEALTHY
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_restart_deployment(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/restart"
        responses.add(
            responses.POST,
            url,
            status=204
        )

        # act
        containers_service.restart(DEPLOYMENT_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_get_scaling_options(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/scaling"
        responses.add(
            responses.GET,
            url,
            json=DEPLOYMENT_DATA["scaling"],
            status=200
        )

        # act
        scaling_options = containers_service.get_scaling_options(
            DEPLOYMENT_NAME)

        # assert
        assert isinstance(scaling_options, ScalingOptions)
        assert scaling_options.min_replica_count == 1
        assert scaling_options.max_replica_count == 3
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_update_scaling_options(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/scaling"
        responses.add(
            responses.PATCH,
            url,
            json=DEPLOYMENT_DATA["scaling"],
            status=200
        )

        # create scaling options object
        scaling_options = ScalingOptions(
            min_replica_count=1,
            max_replica_count=5,
            scale_down_policy=ScalingPolicy(delay_seconds=300),
            scale_up_policy=ScalingPolicy(delay_seconds=60),
            queue_message_ttl_seconds=3600,
            concurrent_requests_per_replica=10,
            scaling_triggers=ScalingTriggers(
                queue_load=QueueLoadScalingTrigger(threshold=0.75),
                cpu_utilization=UtilizationScalingTrigger(
                    enabled=True, threshold=0.8),
                gpu_utilization=UtilizationScalingTrigger(enabled=False)
            )
        )

        # act
        updated_scaling = containers_service.update_scaling_options(
            DEPLOYMENT_NAME, scaling_options)

        # assert
        assert isinstance(updated_scaling, ScalingOptions)
        assert updated_scaling.min_replica_count == 1
        assert updated_scaling.max_replica_count == 3
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_get_replicas(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/replicas"
        responses.add(
            responses.GET,
            url,
            json=REPLICAS_DATA,
            status=200
        )

        # act
        replicas = containers_service.get_replicas(DEPLOYMENT_NAME)

        # assert
        assert "replicas" in replicas
        assert len(replicas["replicas"]) == 1
        assert replicas["replicas"][0]["id"] == "replica-1"
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_purge_queue(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/purge-queue"
        responses.add(
            responses.POST,
            url,
            status=204
        )

        # act
        containers_service.purge_queue(DEPLOYMENT_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_pause_deployment(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/pause"
        responses.add(
            responses.POST,
            url,
            status=204
        )

        # act
        containers_service.pause(DEPLOYMENT_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_resume_deployment(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/resume"
        responses.add(
            responses.POST,
            url,
            status=204
        )

        # act
        containers_service.resume(DEPLOYMENT_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_get_environment_variables(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/environment-variables"
        responses.add(
            responses.GET,
            url,
            json=ENV_VARS_DATA,
            status=200
        )

        # act
        env_vars = containers_service.get_environment_variables(
            DEPLOYMENT_NAME)

        # assert
        assert env_vars["container_name"] == CONTAINER_NAME
        assert len(env_vars["env"]) == 1
        assert env_vars["env"][0]["name"] == "ENV_VAR1"
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_add_environment_variables(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/environment-variables"
        responses.add(
            responses.POST,
            url,
            json=ENV_VARS_DATA,
            status=200
        )

        # act
        env_vars = [{"name": ENV_VAR_NAME,
                     "value_or_reference_to_secret": ENV_VAR_VALUE, "type": "plain"}]
        result = containers_service.add_environment_variables(
            DEPLOYMENT_NAME, CONTAINER_NAME, env_vars)

        # assert
        assert result["container_name"] == CONTAINER_NAME
        assert len(result["env"]) == 1
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_update_environment_variables(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/environment-variables"
        responses.add(
            responses.PATCH,
            url,
            json=ENV_VARS_DATA,
            status=200
        )

        # act
        env_vars = [{"name": ENV_VAR_NAME,
                     "value_or_reference_to_secret": ENV_VAR_VALUE, "type": "plain"}]
        result = containers_service.update_environment_variables(
            DEPLOYMENT_NAME, CONTAINER_NAME, env_vars)

        # assert
        assert result["container_name"] == CONTAINER_NAME
        assert len(result["env"]) == 1
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_delete_environment_variables(self, containers_service, deployments_endpoint):
        # arrange - add response mock
        url = f"{deployments_endpoint}/{DEPLOYMENT_NAME}/environment-variables"
        responses.add(
            responses.DELETE,
            url,
            json={"container_name": CONTAINER_NAME, "env": []},
            status=200
        )

        # act
        result = containers_service.delete_environment_variables(
            DEPLOYMENT_NAME, CONTAINER_NAME, [ENV_VAR_NAME])

        # assert
        assert result["container_name"] == CONTAINER_NAME
        assert len(result["env"]) == 0
        assert responses.assert_call_count(url, 1) is True

    @responses.activate
    def test_get_compute_resources(self, containers_service, compute_resources_endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            compute_resources_endpoint,
            json=COMPUTE_RESOURCES_DATA,
            status=200
        )

        # act
        resources = containers_service.get_compute_resources()

        # assert
        assert type(resources) == list
        assert len(resources) == 2
        assert type(resources[0]) == ComputeResource
        assert resources[0].name == COMPUTE_RESOURCE_NAME
        assert resources[0].size == 1
        assert resources[0].is_available == True
        assert responses.assert_call_count(
            compute_resources_endpoint, 1) is True

    @responses.activate
    def test_get_secrets(self, containers_service, secrets_endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            secrets_endpoint,
            json=SECRETS_DATA,
            status=200
        )

        # act
        secrets = containers_service.get_secrets()

        # assert
        assert type(secrets) == list
        assert len(secrets) == 1
        assert type(secrets[0]) == Secret
        assert secrets[0].name == SECRET_NAME
        assert responses.assert_call_count(secrets_endpoint, 1) is True

    @responses.activate
    def test_create_secret(self, containers_service, secrets_endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            secrets_endpoint,
            json=SECRETS_DATA[0],
            status=200
        )

        # act
        secret = containers_service.create_secret(SECRET_NAME, SECRET_VALUE)

        # assert
        assert type(secret) == Secret
        assert secret.name == SECRET_NAME
        assert responses.assert_call_count(secrets_endpoint, 1) is True

    @responses.activate
    def test_delete_secret(self, containers_service, secrets_endpoint):
        # arrange - add response mock
        url = f"{secrets_endpoint}/{SECRET_NAME}?force=false"
        responses.add(
            responses.DELETE,
            url,
            status=200
        )

        # act
        containers_service.delete_secret(SECRET_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True
        request = responses.calls[0].request
        assert "force=false" in request.url

    @responses.activate
    def test_delete_secret_with_force(self, containers_service, secrets_endpoint):
        # arrange
        url = f"{secrets_endpoint}/{SECRET_NAME}?force=true"
        responses.add(
            responses.DELETE,
            url,
            status=200
        )

        # act
        containers_service.delete_secret(SECRET_NAME, force=True)

        # assert
        assert responses.assert_call_count(url, 1) is True
        request = responses.calls[0].request
        assert "force=true" in request.url

    @responses.activate
    def test_get_registry_credentials(self, containers_service, registry_credentials_endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            registry_credentials_endpoint,
            json=REGISTRY_CREDENTIALS_DATA,
            status=200
        )

        # act
        credentials = containers_service.get_registry_credentials()

        # assert
        assert type(credentials) == list
        assert len(credentials) == 1
        assert type(credentials[0]) == RegistryCredential
        assert credentials[0].name == REGISTRY_CREDENTIAL_NAME
        assert responses.assert_call_count(
            registry_credentials_endpoint, 1) is True

    @responses.activate
    def test_add_registry_credentials(self, containers_service, registry_credentials_endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            registry_credentials_endpoint,
            status=201
        )

        # act
        containers_service.add_registry_credentials(
            REGISTRY_CREDENTIAL_NAME,
            ContainerRegistryType.DOCKERHUB,
            "username",
            "token"
        )

        # assert
        assert responses.assert_call_count(
            registry_credentials_endpoint, 1) is True

    @responses.activate
    def test_add_registry_credentials_validation_error(self, containers_service):
        # act & assert
        with pytest.raises(ValueError) as excinfo:
            containers_service.add_registry_credentials(
                REGISTRY_CREDENTIAL_NAME,
                ContainerRegistryType.DOCKERHUB,
                # Missing username and token
            )
        assert "Username and access_token are required" in str(excinfo.value)

    @responses.activate
    def test_add_registry_credentials_gcr(self, containers_service, registry_credentials_endpoint):
        # arrange
        responses.add(
            responses.POST,
            registry_credentials_endpoint,
            status=201
        )

        # act
        service_account_key = '{"key": "value"}'
        containers_service.add_registry_credentials(
            REGISTRY_CREDENTIAL_NAME,
            ContainerRegistryType.GCR,
            service_account_key=service_account_key
        )

        # assert
        assert responses.assert_call_count(
            registry_credentials_endpoint, 1) is True

    @responses.activate
    def test_add_registry_credentials_aws_ecr(self, containers_service, registry_credentials_endpoint):
        # arrange
        responses.add(
            responses.POST,
            registry_credentials_endpoint,
            status=201
        )

        # act
        containers_service.add_registry_credentials(
            REGISTRY_CREDENTIAL_NAME,
            ContainerRegistryType.AWS_ECR,
            access_key_id="test-key",
            secret_access_key="test-secret",
            region="us-west-2",
            ecr_repo="test.ecr.aws.com"
        )

        # assert
        assert responses.assert_call_count(
            registry_credentials_endpoint, 1) is True

    @responses.activate
    def test_add_registry_credentials_custom(self, containers_service, registry_credentials_endpoint):
        # arrange
        responses.add(
            responses.POST,
            registry_credentials_endpoint,
            status=201
        )

        # act
        docker_config = '{"auths": {"registry.example.com": {"auth": "base64-encoded"}}}'
        containers_service.add_registry_credentials(
            REGISTRY_CREDENTIAL_NAME,
            ContainerRegistryType.CUSTOM,
            docker_config_json=docker_config
        )

        # assert
        assert responses.assert_call_count(
            registry_credentials_endpoint, 1) is True

    @responses.activate
    def test_delete_registry_credentials(self, containers_service, registry_credentials_endpoint):
        # arrange - add response mock
        url = f"{registry_credentials_endpoint}/{REGISTRY_CREDENTIAL_NAME}"
        responses.add(
            responses.DELETE,
            url,
            status=200
        )

        # act
        containers_service.delete_registry_credentials(
            REGISTRY_CREDENTIAL_NAME)

        # assert
        assert responses.assert_call_count(url, 1) is True
