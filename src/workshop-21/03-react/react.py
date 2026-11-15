import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import traceable
from ollama import chat

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()

chat = traceable(chat, run_type="llm", name="ReAct Step")


# Tools
def get_product_price(product: str) -> float:
    """Get the price of a product."""
    prices = {"laptop": 50000, "mouse": 1000, "keyboard": 2000}
    return prices.get(product.lower(), 0)


def calculate_total(price: float, quantity: int) -> float:
    """Calculate total cost from price and quantity."""
    return price * quantity


tools = [get_product_price, calculate_total]
tool_map = {tool.__name__: tool for tool in tools}

messages = [
    {
        "role": "user",
        "content": "What is the total cost of 3 laptops?"
    }
]

# ReAct Loop
steps = 0
MAX_STEPS = 10

while True:
    if steps >= MAX_STEPS:
        print("Maximum steps reached.")
        break

    steps += 1

    response = chat(
          model="qwen3.5:4b",
        messages=messages,
        tools=tools
    )

    messages.append(response.message)

    # No tool calls = Final answer
    if not response.message.tool_calls:
        print("\nFINAL ANSWER:", response.message.content)
        break

    # Execute selected tools
    for call in response.message.tool_calls:
        name = call.function.name
        args = call.function.arguments

        print(f"\nTOOL: {name}({args})")

        result = tool_map[name](**args)

        print("RESULT:", result)

        messages.append({
            "role": "tool",
            "tool_name": name,
            "content": str(result)
        })
