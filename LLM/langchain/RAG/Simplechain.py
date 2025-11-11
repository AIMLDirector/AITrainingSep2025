# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# print(openai_api_key)
prompt = ChatPromptTemplate.from_template("Tell me the latest information about this {topic}.")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, api_key=openai_api_key)   
parser = StrOutputParser()

chain = prompt|llm|parser
value = input("Enter a topic name : ")
response = chain.invoke({"topic": value})
print(response)
