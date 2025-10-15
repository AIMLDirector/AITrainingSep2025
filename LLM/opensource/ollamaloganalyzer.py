import argparse
import requests
import json

def analyze_log(file_path, custom_message=None):
    default_message = "Please analyze this log content and identify error lines with suggestions to fix them."
    prompt_message = custom_message if custom_message else default_message

    # Read the log file
    with open(file_path, 'r') as file:
        log_content = file.read()

    payload = {
        "model": "llama3:latest",  
        "prompt": f"{log_content}\n\n{prompt_message}",
    }

    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        stream=True
    )

    if response.status_code == 200:
        print("Analysis Result:")
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                json_response = json.loads(decoded_line)
                print(json_response["response"], end='', flush=True)
                if json_response.get("done"):
                    break
        print()
    else:
        print(f"Failed to analyze log file. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama Log Analyzer")
    parser.add_argument("file", type=str, help="Path to the log file")
    parser.add_argument("--message", type=str, help="Custom prompt message", default=None)
    args = parser.parse_args()
    analyze_log(args.file, args.message)



