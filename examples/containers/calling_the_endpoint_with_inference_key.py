import os
from datacrunch.InferenceClient import InferenceClient

# Get inference key and endpoint base url from environment variables
DATACRUNCH_INFERENCE_KEY = os.environ.get('DATACRUNCH_INFERENCE_KEY')
DATACRUNCH_ENDPOINT_BASE_URL = os.environ.get('DATACRUNCH_ENDPOINT_BASE_URL')

# Create an inference client that uses only the inference key, without client credentials
inference_client = InferenceClient(
    inference_key=DATACRUNCH_INFERENCE_KEY,
    endpoint_base_url=DATACRUNCH_ENDPOINT_BASE_URL
)

# Make a synchronous request to the endpoint.
# This example demonstrates calling a SGLang deployment which serves LLMs using an OpenAI-compatible API format
data = {
    "model": "deepseek-ai/deepseek-llm-7b-chat",
    "prompt": "Is consciousness fundamentally computational, or is there something more to subjective experience that cannot be reduced to information processing?",
    "max_tokens": 128,
    "temperature": 0.7,
    "top_p": 0.9
}

response = inference_client.run_sync(data=data, path='v1/completions')

# Print the response
print(response.output())
