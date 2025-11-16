from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import RetrievalQA
from langchain.tools import tool
from tavily import TavilyClient # Import the official SDK
import os
import json
from dotenv import load_dotenv

# ===============================
# 🔧 Setup and Initialization
# ===============================
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
travily_api_key = os.getenv("TAVILY_API_KEY")  
print(f"travily_api_key: {travily_api_key}")
print(f"openai_api_key: {openai_api_key}")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, api_key=openai_api_key)


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

        answer = qa.invoke(query)
        return f"Local Search Result:\n{answer}"
    except Exception as e:
        return f"Error in local search: {str(e)}"


@tool("travily_search")
def travily_search(query: str) -> str:
    """Search for travel-related content on the Travily website using the official SDK."""
    try:
        if not travily_api_key:
            return "Travily API key not found in environment variables."

      
        tavily_client = TavilyClient() 

        # Use the SDK's search method
        response = tavily_client.search(query=query, max_results=5) #

        if not response.get("results"):
            return f"No results found for '{query}'."

        results = []
        for item in response["results"]:
            title = item.get("title", "Untitled")
            # The SDK response uses 'content' for the snippet, not 'description'
            desc = item.get("content", "No description.")
            results.append(f"🔹 {title}: {desc}")

        return "Travily API Search Results:\n" + "\n".join(results)

    except Exception as e:
        # The SDK raises specific errors (e.g., InvalidAPIKeyError, UsageLimitExceededError)
        return f"Error searching Travily API with SDK: {str(e)}"


web_search = DuckDuckGoSearchRun(name="web_search")


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

last_message = response['messages'][-1]

# Display as JSON
result = {
    "content": last_message.content,
    "type": last_message.type,
    "additional_kwargs": last_message.additional_kwargs,
    "response_metadata": last_message.response_metadata
}

print(json.dumps(result, indent=2))
