from crewai import Crew,Process
import os
from dotenv import load_dotenv
load_dotenv()
from agent import kafka_agent
from tasks import analyze_kafka_log_task, email_task

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def run():
    crew = Crew(
        agents=[kafka_agent],
        tasks=[analyze_kafka_log_task, email_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    print("\n=== FINAL RESULT ===")
    print(result)

if __name__ == "__main__":
    run()