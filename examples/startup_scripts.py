import os

from datacrunch import DataCrunchClient

# Get client secret and id from environment variables
DATACRUNCH_CLIENT_ID = os.environ.get('DATACRUNCH_CLIENT_ID')
DATACRUNCH_CLIENT_SECRET = os.environ.get('DATACRUNCH_CLIENT_SECRET')

# Create datcrunch client
datacrunch = DataCrunchClient(DATACRUNCH_CLIENT_ID, DATACRUNCH_CLIENT_SECRET)

# Create new startup script
bash_script = """echo this is a test script for serious cat business

# create a cats folder
mkdir cats && cd cats

# download a cat picture
curl https://http.cat/200 --output cat.jpg
"""
script = datacrunch.startup_scripts.create('catty businness', bash_script)

# Print new startup script id, name, script code
print(script.id)
print(script.name)
print(script.script)

# Get all startup scripts
all_scripts = datacrunch.startup_scripts.get()

# Get a single startup script by id
some_script = datacrunch.startup_scripts.get_by_id(script.id)

# Delete startup script by id
datacrunch.startup_scripts.delete_by_id(script.id)
