import os

from verda import VerdaClient

# Get client secret and id from environment variables
CLIENT_ID = os.environ.get('VERDA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('VERDA_CLIENT_SECRET')

# Create datcrunch client
datacrunch = DataCrunchClient(CLIENT_ID, CLIENT_SECRET)

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
