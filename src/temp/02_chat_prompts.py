from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an Deer in the Forest."),
    ("human", "{question}")
])



model = ChatOllama(model="qwen3.5:4b", temperature=0)
chain = prompt | model
response = chain.invoke(
    {"question": "What is RAG?"},
    config={"run_name": "Chat Prompt Example"},
)
print(response.text)
