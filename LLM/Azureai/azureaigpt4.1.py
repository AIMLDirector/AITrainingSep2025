
import os
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv("ENDPOINT_URL", "https://premk-mh8fcwaa-eastus2.cognitiveservices.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# IMAGE_PATH = "YOUR_IMAGE_PATH"
# encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "how to onboard into data engineering module in Azure"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Onboarding into the Data Engineering module in Azure involves several key steps to get you familiar with the tools, services, and best practices for building data pipelines and managing data workflows on the Azure platform. Here’s a structured approach to onboard effectively:\n\n### 1. Understand the Basics of Data Engineering\n- Get a clear understanding of what data engineering entails: data ingestion, data storage, data transformation, and data orchestration.\n- Familiarize yourself with common data engineering concepts such as ETL/ELT, data lakes, data warehouses, batch and stream processing.\n\n### 2. Learn About Azure Data Engineering Services\nAzure offers a variety of services that are essential for data engineering tasks:\n- **Azure Data Factory (ADF):** For data integration and ETL pipelines.\n- **Azure Synapse Analytics:** A unified analytics platform combining data warehousing and big data analytics.\n- **Azure Databricks:** Apache Spark-based analytics platform for big data processing.\n- **Azure Blob Storage / Data Lake Storage Gen2:** For storing large amounts of structured and unstructured data.\n- **Azure Stream Analytics:** For real-time data stream processing.\n- **Azure SQL Database / Azure SQL Data Warehouse:** Managed database services.\n\n### 3. Set Up Your Azure Environment\n- Create an Azure account if you don’t have one.\n- Set up a resource group to organize your Azure resources.\n- Provision the necessary services such as Data Factory, Storage accounts, and Synapse Analytics workspace.\n\n### 4. Hands-On Practice\n- Follow Microsoft Learn modules for data engineering on Azure:\n  - [Introduction to Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/intro-overview)\n  - [Build ETL pipelines with Azure Data Factory](https://learn.microsoft.com/en-us/learn/modules/build-etl-pipelines-with-azure-data-factory/)\n  - [Work with Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/)\n  - [Process data with Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/)\n- Build sample data pipelines: ingest data from various sources, transform it, and load it into a data warehouse or data lake.\n- Experiment with orchestration and scheduling of data workflows.\n\n### 5. Understand Security and Governance\n- Learn about securing data pipelines and storage with Azure Active Directory, managed identities, and role-based access control (RBAC).\n- Understand data governance, data lineage, and monitoring using Azure Monitor and Azure Purview.\n\n### 6. Join Communities and Keep Updated\n- Join Azure data engineering communities on forums such as Microsoft Tech Community, Stack Overflow, and LinkedIn groups.\n- Follow Azure updates and best practices through Microsoft blogs and official documentation.\n\n---\n\n### Summary Checklist for Onboarding:\n- [ ] Learn core data engineering concepts.\n- [ ] Study Azure data engineering services.\n- [ ] Set up Azure environment and services.\n- [ ] Complete hands-on labs and Microsoft Learn modules.\n- [ ] Practice building and orchestrating data pipelines.\n- [ ] Understand security, governance, and monitoring.\n- [ ] Engage with community and keep learning.\n\nIf you want, I can also provide a step-by-step tutorial to build your first Azure Data Factory pipeline or help with specific Azure services!"
            }
        ]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

# Generate the completion
completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    max_tokens=13107,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

print(completion.to_json())
#print(completion.choices.message["content"])
    