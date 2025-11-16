import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
#from langchain.agents import create_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import RetrievalQA
from langchain.tools import tool
from tavily import TavilyClient
import os
import json
from dotenv import load_dotenv

# ===============================
# 🔧 Setup and Initialization
# ===============================
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
travily_api_key = os.getenv("TAVILY_API_KEY")

# Check for API keys
if not openai_api_key:
    st.error("OPENAI_API_KEY not found in environment variables.")
if not travily_api_key:
    st.error("TAVILY_API_KEY not found in environment variables.")

# ===============================
# 🛠️ Tools Definition (Functions are unchanged, wrapped with @tool)
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
        qa = RetrievalQA.from_chain_type(llm=st.session_state.llm, chain_type="stuff", retriever=retriever)

        answer = qa.invoke(query)
        return f"Local Search Result:\n{answer['result']}"
    except Exception as e:
        return f"Error in local search: {str(e)}"


@tool("travily_search")
def travily_search(query: str) -> str:
    """Search for travel-related content on the Travily website using the official SDK."""
    try:
        if not travily_api_key:
            return "Travily API key not found in environment variables."
      
        tavily_client = TavilyClient(api_key=travily_api_key) 

        response = tavily_client.search(query=query, max_results=5)

        if not response.get("results"):
            return f"No results found for '{query}'."

        results = []
        for item in response["results"]:
            title = item.get("title", "Untitled")
            desc = item.get("content", "No description.")
            results.append(f"🔹 {title}: {desc}")

        return "Travily API Search Results:\n" + "\n".join(results)

    except Exception as e:
        return f"Error searching Travily API with SDK: {str(e)}"

web_search = DuckDuckGoSearchRun(name="web_search")
tools = [local_doc_search, travily_search, web_search]

# ===============================
# 🤖 Agent Initialization (moved into a function for Streamlit)
# ===============================

def initialize_agent():
    """Initialize the LangChain agent."""
    if openai_api_key:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, api_key=openai_api_key)
        st.session_state.llm = llm # Store LLM in session state
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant. Use tools when needed to answer queries."),
            ("human", "{input}")
        ])
        # Note: create_agent is for an older version of LangChain. Using an Executor with the new syntax.
        # This requires the user to adapt to the newer LangChain expression language approach, or use the older Agent.from_agent_and_tools
        
        # Using the recommended LCEL approach for agents
        from langchain.agents import AgentExecutor, create_openai_tools_agent
        agent_runnable = create_openai_tools_agent(st.session_state.llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent_runnable, tools=tools, verbose=True)
        st.session_state.agent = agent_executor
    else:
        st.session_state.agent = None

# ===============================
# 🌐 Streamlit UI
# ===============================

st.title("LangChain Multi-Tool Agent App")

# Initialize session state for agent and llm
if 'agent' not in st.session_state:
    initialize_agent()

user_query = st.text_input("Enter your query:", "Investigate Kafka replication log. Search local logs, Travily, and the web for related insights.")

if st.button("Run Agent"):
    if st.session_state.agent and openai_api_key and travily_api_key:
        with st.spinner("Agent is thinking..."):
            try:
                # The agent takes an 'input' key with the user query
                response = st.session_state.agent.invoke({"input": user_query})
                
                # Display the final answer from the agent
                st.subheader("Agent Response:")
                st.write(response['output'])

            except Exception as e:
                st.error(f"An error occurred during agent invocation: {e}")
    else:
        st.warning("Please ensure all API keys are set and the agent is initialized.")
