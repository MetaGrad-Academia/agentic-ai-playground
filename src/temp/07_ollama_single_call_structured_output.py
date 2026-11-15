from langchain_ollama import ChatOllama
from pydantic import BaseModel

MODEL = "qwen3.5:4b"


class Customer(BaseModel):
    name: str
    age: int
    email: str


def main():
    structured_llm = ChatOllama(model=MODEL, temperature=0).with_structured_output(
        Customer
    )
    customer = structured_llm.invoke(
        "Generate a fictional customer profile with a name, age, and email address "
        "using the example.com domain."
    )

    print(customer.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
