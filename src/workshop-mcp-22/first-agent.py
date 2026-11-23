


from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama


def main():

    model = ChatOllama(model="qwen3.5:4b")
    agent = create_agent(model=model)

    user_input = input("You: ").strip()
    result = agent.invoke({"messages": [HumanMessage(content=user_input)]})
    # We use [-1] because the agent's 
    # final answer is normally the last message 
    # in the returned message history.
    print(f"Agent: {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
