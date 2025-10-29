import os

from datacrunch import DataCrunchClient

# Fileset secrets are a way to mount sensitive files like API keys, certs, and credentials securely inside a container, without hardcoding them in the image or env vars.
# This example demonstrates how to create a fileset secret containing two files from your local filesystem

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Initialize the client with your credentials
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Define the secret name and the file paths from your local filesystem where this script is running
SECRET_NAME = 'my-fileset-secret'
RELATIVE_FILE_PATH = './relative-path/file1.txt'
ABSOLUTE_FILE_PATH = '/home/username/absolute-path/file2.json'

# Create the fileset secret that has 2 files
fileset_secret = datacrunch.containers.create_fileset_secret_from_file_paths(
    secret_name=SECRET_NAME, file_paths=[RELATIVE_FILE_PATH, ABSOLUTE_FILE_PATH]
)

# Get the secret
secrets = datacrunch.containers.get_fileset_secrets()
print(secrets)

# Delete the secret
datacrunch.containers.delete_fileset_secret(secret_name=SECRET_NAME)
