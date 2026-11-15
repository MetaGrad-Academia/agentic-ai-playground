import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable
from ollama import chat

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()


QUESTION = (
    "In 2023, WhatsApp introduced a feature called\n"
    '"AI Message Recovery" that lets users recover\n'
    "deleted messages using ChatGPT.\n\n"
    "Explain how this feature works and how to enable it\n"
    "on Android."
)


@traceable(
    run_type="llm",
    name="Hallucination Example",
)
def ask_model(question: str) -> str:
    response = chat(
        model="tinyllama",
        messages=[{"role": "user", "content": question}],
        options={"temperature": 1.2},
    )
    return response.message.content


if __name__ == "__main__":
    print(ask_model(QUESTION))
