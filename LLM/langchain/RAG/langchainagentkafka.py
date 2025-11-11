from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentType, initialize_agent
from dotenv import load_dotenv
import os
import re

#  Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define your Kafka log directory
KAFKA_LOG_PATH = "/Users/premkumargontrand/pythonlearning082025/LLM/langchain/RAG/kafka"  # 👈 change to your actual Kafka log directory


#  List Kafka log files
@tool("list_kafka_logs", return_direct=False)
def list_kafka_logs(directory: str = KAFKA_LOG_PATH) -> str:
    """
    List all Kafka log files in the specified directory.
    Used to identify available logs such as server.log, controller.log, etc.
    """
    try:
        directory = directory.strip().strip("'").strip('"')
        if not os.path.exists(directory):
            return f"Kafka log directory not found: {directory}"

        files = [f for f in os.listdir(directory) if f.endswith(".log")]
        if not files:
            return f"⚠️ No .log files found in: {directory}"
        return "\n".join(files)
    except Exception as e:
        return f"Error listing Kafka logs: {str(e)}"


#  Read a Kafka log file
@tool("read_kafka_log", return_direct=False)
def read_kafka_log(file_name: str) -> str:
    """
    Read the content of a Kafka log file from the Kafka log directory.
    """
    try:
        cleaned_name = file_name.strip().strip("'").strip('"')
        file_path = os.path.join(KAFKA_LOG_PATH, cleaned_name)

        if not os.path.exists(file_path):
            return f"Log file not found: {file_path}"

        with open(file_path, "r") as f:
            content = f.read()

        # Only return last 500 lines to avoid overload
        lines = content.splitlines()
        if len(lines) > 500:
            lines = lines[-500:]
            content = "\n".join(lines)

        return f"✅ Last 500 lines of {cleaned_name}:\n\n{content}"
    except Exception as e:
        return f"Error reading Kafka log file: {str(e)}"


# Analyze Kafka log content
@tool("analyze_kafka_log", return_direct=False)
def analyze_kafka_log(log_content: str) -> str:
    """
    Analyze Kafka log content and highlight common issues such as broker startup errors,
    ZooKeeper connection failures, or replication issues.
    """
    try:
        log_content = log_content.lower()

        patterns = {
            "ZooKeeper Connection Failure": r"zookeeper.*(failed|disconnected|error)",
            "Broker Startup Failure": r"fatal|exception.*broker",
            "Replication Issue": r"replica.*error",
            "Out of Memory": r"outofmemory|oom",
            "Port Binding Issue": r"bindexception|address already in use",
            "Authorization Error": r"auth.*fail|sasl.*error",
        }

        detected = []
        for issue, pattern in patterns.items():
            if re.search(pattern, log_content):
                detected.append(f"⚠️ {issue} detected")

        if not detected:
            return "No critical Kafka errors detected in the logs."

        return "Detected Kafka issues:\n" + "\n".join(detected)
    except Exception as e:
        return f"Error analyzing Kafka log: {str(e)}"


#  Create the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=openai_api_key
)

# Initialize the agent
agent = initialize_agent(
    tools=[list_kafka_logs, read_kafka_log, analyze_kafka_log],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

#  Example workflow
query = (
    "List all Kafka log files in the directory, "
    "read 'server.log', and analyze it for common Kafka errors."
)

output = agent.invoke(query)

print("\n--- Kafka Log Analysis Result ---\n")
print(output)
