from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    age: int
    email: str


def main():
    agent = create_agent(
        model=ChatOllama(model="qwen3.5:4b", temperature=0),
        response_format=Customer,
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "John is 25 years old. His email is john@example.com.",
                }
            ]
        }
    )

    customer = result["structured_response"]
    print(customer)


if __name__ == "__main__":
    main()
