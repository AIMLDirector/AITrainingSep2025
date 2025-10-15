import ollama

response = ollama.generate(model='llama3.2:latest', prompt='what is a qubit?')
print(response['response'])