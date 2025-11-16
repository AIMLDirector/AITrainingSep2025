import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain.tools import tool
from bs4 import BeautifulSoup
import requests
import os
import json
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType

# ==========================================================
# Load environment variables
# ==========================================================
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
travily_api_key = os.getenv("TRAVILY_API_KEY")

# ==========================================================
# Streamlit UI setup
# ==========================================================
st.set_page_config(page_title="AI Multi-Tool Agent", layout="wide")
st.title("🧠 AI Knowledge Agent – Multi Source Search")
st.caption("Uses local documents, Travily, and web search tools to answer questions.")

# ==========================================================
# LLM setup
# ==========================================================
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4, api_key=openai_api_key)

# ==========================================================
# Define Tools
# ==========================================================
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


@tool("travily_search")
def travily_search(query: str) -> str:
    """Search for travel-related content on the Travily website."""
    try:
        url = f"https://www.travily.com/search?q={requests.utils.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        for item in soup.select("article, .search-result, .post-item"):
            title_tag = item.select_one("h2, h3, .title")
            desc_tag = item.select_one("p, .excerpt, .summary")
            if title_tag and desc_tag:
                title = title_tag.get_text(strip=True)
                desc = desc_tag.get_text(strip=True)
                results.append(f"🔹 {title}: {desc}")

        if not results:
            return "No results found on Travily."
        return "Travily Search Results:\n" + "\n".join(results[:5])
    except Exception as e:
        return f"Error searching Travily: {str(e)}"


web_search = DuckDuckGoSearchRun(name="web_search")

# List of tools
tools = [local_doc_search, travily_search, web_search]

# ==========================================================
# Initialize agent (compatible with LangChain 1.0.3)
# ==========================================================
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# ==========================================================
# Streamlit Input + Execution
# ==========================================================
user_query = st.text_area(
    "💬 Ask your question:",
    placeholder="E.g. Investigate Kafka replication lag using local docs, Travily, and the web...",
    height=120
)

if st.button("Run Agent 🚀", use_container_width=True):
    if not user_query.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Running agent... please wait ⏳"):
            try:
                response = agent.run(user_query)
                st.success("✅ Agent completed successfully!")
                st.markdown("### 🧩 Response:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ==========================================================
# Debug / Raw Output section
# ==========================================================
with st.expander("🪄 Debug Info"):
    st.json({
        "tools_enabled": [t.name for t in tools],
        "model": llm.model_name,
        "temperature": llm.temperature
    })

st.dropdown_menu = st.sidebar.selectbox(
    "Select Generation Parameters Preset",
    ["Default", "Creative", "Precise"]
)