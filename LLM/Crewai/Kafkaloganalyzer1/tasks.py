from crewai import Task
import os
from dotenv import load_dotenv
load_dotenv()
from agent import kafka_agent
from tools.log_reader import read_log_file
from tools.mail_sender import email_sender_tool

LOG_FILE = "./kafka.log"

def read_kafka_logs(path: str):
    collected_logs = ""

    if not os.path.exists(path):
        return f"Path not found: {path}"

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".log"):
                file_path = os.path.join(root, f)
                with open(file_path, "r", errors="ignore") as fp:
                    collected_logs += f"\n\n==== FILE: {file_path} ====\n"
                    collected_logs += fp.read()

    return collected_logs

log_data = read_kafka_logs(LOG_FILE)

analyze_kafka_log_task = Task(
    description=(
        f"Analyze the following Kafka log data and return actionable insights, "
        f"including errors, root cause hints, warnings, GC issues, ISR problems, "
        f"network delays, authentication failures, or instability patterns.\n\n"
        f"=== LOG DATA START ===\n{log_data}\n=== LOG DATA END ==="
    ),
    agent=kafka_agent,
    expected_output="Detailed analysis of Kafka logs with recommended fixes.",
    tools=[read_log_file]
)

email_task = Task(
    description=(
        "Send the analysis summary using EmailSender tool. "
        "Use the tool to send an email containing the findings."
    ),
    expected_output="A confirmation message that the email was sent.",
    agent=kafka_agent,
    tools=[email_sender_tool],
    context=[analyze_kafka_log_task]
)