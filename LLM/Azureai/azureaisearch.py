
import os
import base64
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "https://premk-mh1mwk6d-eastus2.cognitiveservices.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-mini")
search_endpoint = os.getenv("SEARCH_ENDPOINT", "https://aisearchservicepragathi.search.windows.net")
search_key = os.getenv("SEARCH_KEY", "")
search_index = os.getenv("SEARCH_INDEX_NAME", "search-1761115257574")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

user_query = input("Enter your question: ")

# === Chat Prompt ===
chat_prompt = [
    {
        "role": "system",
        "content": [
            {"type": "text", "text": "You are an AI assistant that helps users find information from Azure Cognitive Search."}
        ],
    },
    {
        "role": "user",
        "content": [{"type": "text", "text": user_query}],
    },
]



completion = client.chat.completions.create(
    model=deployment,
    messages=chat_prompt,
    data_sources=[
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_endpoint,
                "index_name": search_index,
                "authentication": {
                    "type": "api_key",
                    "key": search_key
                }
            }
        }
    ]
)

# === Display the response ===
print("\nAI Response:")
print(completion.choices[0].message["content"])
    