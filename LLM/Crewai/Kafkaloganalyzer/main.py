from crewai import Crew
import os
from dotenv import load_dotenv
load_dotenv()
from agent_kafka import kafka_agent
from tasks_kafka import analyze_kafka_log_task

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def run():
    crew = Crew(
        agents=[kafka_agent],
        tasks=[analyze_kafka_log_task],
        verbose=True
    )

    result = crew.kickoff()
    print("\n=== FINAL RESULT ===")
    print(result)

if __name__ == "__main__":
    run()