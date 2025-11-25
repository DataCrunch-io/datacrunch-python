import os
from time import sleep

from verda import VerdaClient
from verda.InferenceClient.inference_client import AsyncStatus

# Configuration - replace with your deployment name
DEPLOYMENT_NAME = os.environ.get('VERDA_DEPLOYMENT_NAME')

# Get client secret and id from environment variables
CLIENT_ID = os.environ.get('VERDA_CLIENT_ID')
CLIENT_SECRET = os.environ.get('VERDA_CLIENT_SECRET')
INFERENCE_KEY = os.environ.get('VERDA_INFERENCE_KEY')

# DataCrunch client instance
datacrunch = DataCrunchClient(
    CLIENT_ID,
    CLIENT_SECRET,
    inference_key=INFERENCE_KEY,
)

# Get the deployment
deployment = datacrunch.containers.get_deployment_by_name(DEPLOYMENT_NAME)

# Make an asynchronous request to the endpoint.
# This example demonstrates calling a SGLang deployment which serves LLMs using an OpenAI-compatible API format
data = {
    'model': 'deepseek-ai/deepseek-llm-7b-chat',
    'prompt': 'Is consciousness fundamentally computational, or is there something more to subjective experience that cannot be reduced to information processing?',
    'max_tokens': 128,
    'temperature': 0.7,
    'top_p': 0.9,
}

header = {'Content-Type': 'application/json'}

response = deployment.run(
    data=data,
    path='v1/completions',
    headers=header,
)

while response.status() != AsyncStatus.Completed:
    print(response.status_json())
    sleep(1)
print(response.output())
