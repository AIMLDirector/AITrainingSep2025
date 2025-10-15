import requests
import json

url = "http://localhost:11434/api/generate"
prompt = input("Please enter your prompt: ")  # Ask for prompt input
payload = {
    "model": "deepseek-r1:1.5b",
    "prompt": prompt,  # Use the user input for the prompt
    "stream": False
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print(data["response"])  
else:
    print(f"Error: {response.status_code}")
    print(response.text)