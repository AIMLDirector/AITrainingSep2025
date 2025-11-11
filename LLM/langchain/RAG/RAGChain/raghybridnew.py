from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_classic.chains import RetrievalQA
from langchain.tools import tool
from bs4 import BeautifulSoup
import requests
import os
import json
from dotenv import load_dotenv

# ===============================
# 🔧 Setup and Initialization
# ===============================
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
travily_api_key = os.getenv("TRAVILY_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, api_key=openai_api_key)

# ===============================
# 🧠 Tool 1: Local Document Search
# ===============================
@tool("local_doc_search")
def local_doc_search(query: str, directory: str = "./data") -> str:
    """Search for answers in local PDF or TXT documents within the given directory."""
    try:
        if not os.path.exists(directory):
            return f"Directory not found: {directory}"

        docs = []
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if file.endswith(".txt"):
                docs.extend(TextLoader(path).load())
            elif file.endswith(".pdf"):
                docs.extend(PyPDFLoader(path).load())

        if not docs:
            return f"No readable files found in {directory}"

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = splitter.split_documents(docs)

        embeddings = OpenAIEmbeddings(api_key=openai_api_key)
        vectorstore = FAISS.from_documents(splits, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

        answer = qa.run(query)
        return f"Local Search Result:\n{answer}"
    except Exception as e:
        return f"Error in local search: {str(e)}"

# ===============================
# 🌍 Tool 2: Travily Web Search
# ===============================
@tool("travily_search")
def travily_search(query: str) -> str:
    """Search for travel-related content on the Travily website."""
    try:
        url = "https://api.travily.com/v1/search"
        headers = {
            "Authorization": f"Bearer {travily_api_key}",  # or "x-api-key" if Travily uses that format
            "Content-Type": "application/json",
        }
        params = {"q": query, "limit": 5}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            return f"No results found for '{query}'."

        results = []
        for item in data["results"]:
            title = item.get("title", "Untitled")
            desc = item.get("description", "No description.")
            results.append(f"🔹 {title}: {desc}")

        return "Travily API Search Results:\n" + "\n".join(results)

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error searching Travily API: {str(e)}"

# ===============================
# 🔎 Tool 3: General Web Search
# ===============================
web_search = DuckDuckGoSearchRun(name="web_search")

# ===============================
# 🤖 Create Agent (LangChain 1.x)
# ===============================
tools = [local_doc_search, travily_search, web_search]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant. Use tools when needed to answer queries."),
    ("human", "{input}")
])

agent = create_agent(
    model="gpt-4o-mini",
    tools=tools,
    system_prompt="You are an AI assistant. Use tools when needed to answer queries."
)

query = "Investigate Kafka replication log. Search local logs, Travily, and the web for related insights."
response = agent.invoke({"messages": [{"role": "user", "content": query}]})
# print(response)



last_message = response['messages'][-1]

# Display as JSON
result = {
    "content": last_message.content,
    "type": last_message.type,
    "additional_kwargs": last_message.additional_kwargs,
    "response_metadata": last_message.response_metadata
}

print(json.dumps(result, indent=2))