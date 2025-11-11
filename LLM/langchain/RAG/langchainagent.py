from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentType, initialize_agent
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


BASE_PATH = "/Users/premkumargontrand/pythonlearning082025/LLM/langchain/RAG"

@tool("list_files", return_direct=False)
def list_files(directory: str= BASE_PATH) -> str:
    """
    List all files and folders in the specified directory path.
    This tool returns the names of all files and subdirectories under the given path.
    """
    try:
        directory = directory.strip().strip("'").strip('"')  
        if not os.path.exists(directory):
            return f" Directory not found: {directory}"
        files = os.listdir(directory)
        if not files:
            return f"⚠️ No files found in: {directory}"
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool("read_file", return_direct=False)
def read_file(file_name: str) -> str:
    """
    Read the content of a file from the predefined base path.
    Provide the file name (e.g., 'example.txt') to read its content.
    """
    try:
        cleaned_name = file_name.strip().strip("'").strip('"')
        file_path = os.path.join(BASE_PATH, cleaned_name)
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        with open(file_path, "r") as file:
            content = file.read()
        return f" Content of {file_name}:\n\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=openai_api_key) 

agent = initialize_agent(
    tools=[list_files, read_file],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

query = (
    "List all files in the specific directory, "
    "then read the content of the file named 'example.txt'."
)

output = agent.invoke(query)
print(output)  

