import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent
from tools.log_reader import read_log_file
from tools.mail_sender import email_sender_tool


kafka_agent = Agent(

    name="KafkaLogAnalyzer",
    role="Kafka Log Analysis Expert",
    llm="openai/gpt-4o-mini" ,
    tools=[read_log_file, email_sender_tool],
    goal=(
        "Analyze kafka server logs from a given file path, "
        "detect anomalies, errors, warnings, unexpected restarts, "
        "and summarize findings with recommended actions."
    ),
    backstory=(
        "You are an expert in distributed systems, Kafka clusters, "
        "and log pattern analysis. You understand how to identify issues "
        "like broker failures, GC pauses, ISR shrink/expansion, "
        "leader election errors, and message handling failures."
    )
)