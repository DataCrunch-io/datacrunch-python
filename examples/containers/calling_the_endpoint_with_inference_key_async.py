import os
from time import sleep
from datacrunch.InferenceClient import InferenceClient
from datacrunch.InferenceClient.inference_client import AsyncStatus

# Get inference key and endpoint base url from environment variables
DATACRUNCH_INFERENCE_KEY = os.environ.get('DATACRUNCH_INFERENCE_KEY')
DATACRUNCH_ENDPOINT_BASE_URL = os.environ.get('DATACRUNCH_ENDPOINT_BASE_URL')

# Create an inference client that uses only the inference key, without client credentials
inference_client = InferenceClient(
    inference_key=DATACRUNCH_INFERENCE_KEY,
    endpoint_base_url=DATACRUNCH_ENDPOINT_BASE_URL,
)

# Make an asynchronous request to the endpoint
# This example demonstrates calling a SGLang deployment which serves LLMs using an OpenAI-compatible API format
data = {
    'model': 'deepseek-ai/deepseek-llm-7b-chat',
    'prompt': 'Is consciousness fundamentally computational, or is there something more to subjective experience that cannot be reduced to information processing?',
    'max_tokens': 128,
    'temperature': 0.7,
    'top_p': 0.9,
}

# Run the request asynchronously using the inference client
async_inference_execution = inference_client.run(data=data, path='v1/completions')

# Poll for status until completion
while async_inference_execution.status() != AsyncStatus.Completed:
    print(async_inference_execution.status_json())
    sleep(5)

# Print the response
print(async_inference_execution.output())
