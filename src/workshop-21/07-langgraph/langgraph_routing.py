import sys
from pathlib import Path
from typing import Literal, TypedDict

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from configurations import http_config  # noqa: E402, F401

load_dotenv()

# Example: AI Customer Support Routing
#
#                    Customer Question
#                            |
#                            v
#                   +------------------+
#                   |   AI Classifier  |
#                   | Billing/Technical|
#                   +------------------+
#                            |
#                  +---------+---------+
#                  |                   |
#              Billing              Technical
#                  |                   |
#                  v                   v
#          +---------------+   +----------------+
#          | Billing Agent |   | Technical Agent|
#          | Payments &    |   | Errors & Bugs  |
#          | Refunds       |   |                |
#          +---------------+   +----------------+
#                  |                   |
#                  +---------+---------+
#                            |
#                            v
#                    +----------------+
#                    | Final Response |
#                    +----------------+



llm = ChatOllama(model="qwen3.5:4b", temperature=0)


# Shared state
class State(TypedDict):
    question: str
    category: str
    answer: str


# Step 1: AI decides the category
def classify(state: State):
    response = llm.invoke(
        "Classify this customer question as BILLING or TECHNICAL. "
        "Reply with only one word.\n"
        f"Question: {state['question']}"
    )

    category = response.content.strip().upper()
    return {
        "category": "BILLING" if category == "BILLING"
        else "TECHNICAL"
    }


# Step 2A: Billing agent
def billing_agent(state: State):
    response = llm.invoke(
        "You are a billing support agent. "
        "Give a short helpful answer. "
        "Do not invent account details.\n"
        f"Question: {state['question']}"
    )
    return {"answer": response.content}


# Step 2B: Technical agent
def technical_agent(state: State):
    response = llm.invoke(
        "You are a technical support agent. "
        "Give a short troubleshooting answer.\n"
        f"Question: {state['question']}"
    )
    return {"answer": response.content}


# Conditional routing
def route(state: State) -> Literal["billing", "technical"]:
    return "billing" if state["category"] == "BILLING" else "technical"


# Build graph
graph = StateGraph(State)

graph.add_node("classify", classify)
graph.add_node("billing", billing_agent)
graph.add_node("technical", technical_agent)

graph.add_edge(START, "classify")

graph.add_conditional_edges(
    "classify",
    route,
    {
        "billing": "billing",
        "technical": "technical"
    }
)

graph.add_edge("billing", END)
graph.add_edge("technical", END)

app = graph.compile()


# Run workflow
result = app.invoke({
    "question": "My payment was deducted twice.",
    "category": "",
    "answer": ""
}, config={"run_name": "LangGraph Support Routing"})

print("Category:", result["category"])
print("Answer:", result["answer"])
