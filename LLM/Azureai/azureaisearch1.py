from openai import OpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os

# --- Azure Cognitive Search setup ---
search_endpoint = "https://aisearchservicepragathi.search.windows.net"
search_index = "search-1761115257574"
search_key = ""

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=search_index,
    credential=AzureKeyCredential(search_key),
)

# --- Query the index ---
user_query = input("Enter your question: ")
results = search_client.search(search_text=user_query)

# Gather relevant context
context = ""
for result in results:
    context += result.get("content", "") + "\n"

# --- Call OpenAI (standard model) ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = f"""
You are a helpful assistant that answers questions using the following context:

{context}

Question: {user_query}
Answer:
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)

print("\nAI Response:")
print(completion.choices[0].message.content)
