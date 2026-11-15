from langchain_ollama import ChatOllama
from pydantic import BaseModel

MODEL = "qwen3.5:4b"


class Customer(BaseModel):
    name: str
    age: int
    email: str


def main():
    text_model = ChatOllama(model=MODEL, temperature=0.7)
    generated_text = text_model.invoke(
        "Create a fictional customer profile in one sentence. Include a name, "
        "age, and an email address using the example.com domain."
    ).content

    print("Free-form model output:")
    print(generated_text)

    structured_model = ChatOllama(model=MODEL, temperature=0).with_structured_output(
        Customer
    )
    customer = structured_model.invoke(
        "Extract the name, age, and email from this text. Do not invent missing details.\n\n"
        f"{generated_text}"
    )

    print("\nStructured model output:")
    print(customer)


if __name__ == "__main__":
    main()
