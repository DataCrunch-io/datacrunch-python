import os
from datacrunch import DataCrunchClient

# Get client secret from environment variable
CLIENT_SECRET = os.environ['DATACRUNCH_CLIENT_SECRET']
CLIENT_ID = 'Ibk5bdxV64lKAWOqYnvSi'  # Replace with your client ID

# Create datcrunch client
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

# Create instance with extra volumes
# TODO:

# Create instance with existing OS volume as an image
# TODO:

# Delete instance without deleting the OS volume
# TODO:

# Delete instance and one of it's volumes
# TODO:

