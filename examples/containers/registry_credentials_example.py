import os
from datacrunch import DataCrunchClient
from datacrunch.containers.containers import ContainerRegistryType

# Environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Initialize DataCrunch client
datacrunch_client = DataCrunchClient(client_id=DATACRUNCH_CLIENT_ID,
                                     client_secret=DATACRUNCH_CLIENT_SECRET)

# Example 1: DockerHub Credentials
datacrunch_client.containers.add_registry_credentials(
    name="my-dockerhub-creds",
    registry_type=ContainerRegistryType.DOCKERHUB,
    username="your-dockerhub-username",
    access_token="your-dockerhub-access-token"
)
print("Created DockerHub credentials")

# Example 2: GitHub Container Registry Credentials
datacrunch_client.containers.add_registry_credentials(
    name="my-github-creds",
    registry_type=ContainerRegistryType.GITHUB,
    username="your-github-username",
    access_token="your-github-token"
)
print("Created GitHub credentials")

# Example 3: Google Container Registry (GCR) Credentials
# For GCR, you need to provide a service account key JSON string
gcr_service_account_key = """{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY_HERE\\n-----END PRIVATE KEY-----\\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}"""

datacrunch_client.containers.add_registry_credentials(
    name="my-gcr-creds",
    registry_type=ContainerRegistryType.GCR,
    service_account_key=gcr_service_account_key
)
print("Created GCR credentials")

# Example 4: AWS ECR Credentials
datacrunch_client.containers.add_registry_credentials(
    name="my-aws-ecr-creds",
    registry_type=ContainerRegistryType.AWS_ECR,
    access_key_id="your-aws-access-key-id",
    secret_access_key="your-aws-secret-access-key",
    region="us-west-2",
    ecr_repo="123456789012.dkr.ecr.us-west-2.amazonaws.com"
)
print("Created AWS ECR credentials")

# Example 5: Custom Registry Credentials
custom_docker_config = """{
  "auths": {
    "your-custom-registry.com": {
      "auth": "base64-encoded-username-password"
    }
  }
}"""

datacrunch_client.containers.add_registry_credentials(
    name="my-custom-registry-creds",
    registry_type=ContainerRegistryType.CUSTOM,
    docker_config_json=custom_docker_config
)
print("Created Custom registry credentials")

# Delete all registry credentials
datacrunch_client.containers.delete_registry_credentials('my-dockerhub-creds')
datacrunch_client.containers.delete_registry_credentials('my-github-creds')
datacrunch_client.containers.delete_registry_credentials('my-gcr-creds')
datacrunch_client.containers.delete_registry_credentials('my-aws-ecr-creds')
datacrunch_client.containers.delete_registry_credentials(
    'my-custom-registry-creds')
