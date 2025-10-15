import ollama
import subprocess

MODEL_NAME = "gemma:2b"
PROMPT = "What is a qubit?"

def model_exists(model_name: str) -> bool:
    """Check if the model exists locally using 'ollama list'."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return model_name in result.stdout
    except Exception as e:
        print(f"⚠️  Could not check model list: {e}")
        return False

def pull_model(model_name: str):
    """Download the model if it doesn't exist."""
    print(f"⬇️  Downloading model: {model_name} ...")
    subprocess.run(["ollama", "pull", model_name], check=True)
    print("✅ Model downloaded successfully.\n")

def main():
    # Ensure Ollama server is running
    try:
        ollama_version = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if ollama_version.returncode != 0:
            raise Exception("Ollama CLI not found. Make sure Ollama is installed and added to PATH.")
    except FileNotFoundError:
        print("❌ Ollama is not installed or not in PATH.")
        return

    # Check and pull model if necessary
    if not model_exists(MODEL_NAME):
        pull_model(MODEL_NAME)
    else:
        print(f"✅ Model '{MODEL_NAME}' already available.\n")

    # Generate response
    print(f"🧠 Running model '{MODEL_NAME}'...\n")
    try:
        response = ollama.generate(model=MODEL_NAME, prompt=PROMPT, stream=False)
        print("📝 Output:\n")
        print(response["response"])
    except Exception as e:
        print(f"❌ Error generating response: {e}")

if __name__ == "__main__":
    main()
