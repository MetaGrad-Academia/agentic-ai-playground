
from langchain.tools import tool

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama

@tool
def process_refund():
    """Provide instructions for requesting a refund."""
    return "To get a refund, please contact our support team with your order details."

@tool
def process_exchange():
    """Provide instructions for requesting an exchange."""
    return "To process an exchange, please provide your order details and the item you wish to exchange."

@tool
def process_return():
    """Provide instructions for requesting a return."""
    return "To process a return, please provide your order details and the item you wish to return."    

def main():

    model = ChatOllama(model="gemma4:12b", num_ctx=16384)
    agent = create_agent(model=model, tools=[process_refund, 
    process_exchange, process_return]
    )

    user_input = input("You: ").strip()
    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
    # We use [-1] because the agent's 
    # final answer is normally the last message 
    # in the returned message history.
    print(f"Agent: {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
