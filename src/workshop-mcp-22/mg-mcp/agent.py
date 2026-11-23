import asyncio

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_core.tools import StructuredTool
from langchain_ollama import ChatOllama

from mcp_client import connect, disconnect, discover_tools, execute_tool


def to_langchain_tool(client, mcp_tool):
    # Wrap an MCP tool so the LangChain agent can call it.
    async def run(**kwargs):
        result = await execute_tool(client, mcp_tool.name, kwargs)
        return result.content[0].text

    return StructuredTool.from_function(
        coroutine=run,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        args_schema=mcp_tool.inputSchema,
    )


async def main():
    client = await connect()

    mcp_tools = await discover_tools(client)
    tools = [to_langchain_tool(client, t) for t in mcp_tools]

    model = ChatOllama(model="gemma4:12b")
    agent = create_agent(model=model, tools=tools)

    user_input = input("You: ").strip()
    result = await agent.ainvoke({"messages": [HumanMessage(content=user_input)]})
    # We use [-1] because the agent's
    # final answer is normally the last message
    # in the returned message history.
    print(f"Agent: {result['messages'][-1].content}")

    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
