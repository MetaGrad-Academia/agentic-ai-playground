import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()


@tool
def get_product_price(product: str) -> int:
    """Get the price of a product."""
    return {"laptop": 50000, "mouse": 1000}.get(product, 0)


@tool
def calculate_total(price: int, quantity: int) -> int:
    """Calculate the total price."""
    return price * quantity


agent = create_agent(
    model=ChatOllama(model="qwen3.5:4b", temperature=0),
    tools=[get_product_price, calculate_total],
    system_prompt="Use the provided tools to look up prices and calculate totals."
)

response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What is the cost of 3 laptops?"}
        ]
    },
    config={"recursion_limit": 10, "run_name": "LangChain Agent Example"}
)

print(response["messages"][-1].content)
