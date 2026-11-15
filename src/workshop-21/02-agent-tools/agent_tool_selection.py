import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable
from ollama import chat

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()

chat = traceable(chat, run_type="llm", name="Agent Tool Selection")


def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return f"Calculating: {expression}"


def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"Checking weather in {city}"


def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Searching: {query}"


questions = [
    "What is 25 multiplied by 48?",
    "What's the weather in Chennai?",
    "Find the latest news about NVIDIA."
]

for question in questions:
    response = chat(
        model="qwen3.5:4b",
        messages=[{"role": "user", "content": question}],
        tools=[calculate, get_weather, search_web],
    )

    print(f"\nUSER: {question}")

    for call in response.message.tool_calls or []:
        print("SELECTED TOOL:", call.function.name)
        print("ARGUMENTS:", call.function.arguments)
