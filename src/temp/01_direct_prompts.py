from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

load_dotenv()
information = "Barack Obama"
summary_template = """

    Given the information {information} about a person, create:

    1. A short summary
    2. Two interesting facts about them

    """

summary_prompt_template = PromptTemplate(
    input_variables=["information"], template=summary_template
)

llm = ChatOllama(temperature=0, model="qwen3.5:4b")
chain = summary_prompt_template | llm
response = chain.invoke(input={"information": information},
  config={"run_name": "Chat Prompt Example"})
print(response.text)
