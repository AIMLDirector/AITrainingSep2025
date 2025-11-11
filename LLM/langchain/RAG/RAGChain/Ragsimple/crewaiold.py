# crew_rag.py
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

# --- Setup retriever ---
CHROMA_DIR = "./chroma_db"
embedding = OpenAIEmbeddings()
vectordb = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embedding,
)
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# --- LLM ---
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- Agents ---
researcher = Agent(
    role="Researcher",
    goal="Look up information in the knowledge base using retrieval.",
    backstory="An expert at finding relevant context in documents.",
    allow_delegation=False,
    llm=llm,
)

writer = Agent(
    role="Writer",
    goal="Answer the user's question clearly using the provided research context.",
    backstory="A skilled communicator who summarizes research into clear answers.",
    allow_delegation=False,
    llm=llm,
)

# --- Tasks ---
def retrieval_task(question: str):
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    return Task(
        description=f"Retrieve relevant knowledge for: {question}\n\nContext:\n{context}",
        expected_output="A concise set of relevant facts.",
        agent=researcher,
    )

def answer_task(question: str):
    return Task(
        description=f"Write a clear answer to the question: {question}",
        expected_output="A well-written final answer.",
        agent=writer,
    )

def run_crew(question: str):
    crew = Crew(
        agents=[researcher, writer],
        tasks=[retrieval_task(question), answer_task(question)],
        process=Process.sequential,  # researcher first, writer second
    )
    return crew.kickoff()

if __name__ == "__main__":
    while True:
        q = input("Q: ")
        if q.lower() in ("exit", "quit"):
            break
        result = run_crew(q)
        print("\n🤖 Answer:", result, "\n")
