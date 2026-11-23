# Step 4: One agent, three MCP servers. The LLM picks which one to use.
import asyncio
import os
from contextlib import AsyncExitStack
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama

PROJECT_DIR = str(Path(__file__).resolve().parent.parent)


async def main():
    load_dotenv()

    servers = {
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", PROJECT_DIR],
        },
        "playwright": {
            "transport": "stdio",
            "command": "npx",
            "args": ["@playwright/mcp@latest", "--headless"],
        },
    }

    # GitHub is optional: only added when GITHUB_TOKEN is set in .env.
    if os.getenv("GITHUB_TOKEN"):
        github_write_enabled = os.getenv("GITHUB_ENABLE_WRITE", "").lower() == "true"
        github_url = "https://api.githubcopilot.com/mcp/x/repos"
        if not github_write_enabled:
            github_url += "/readonly"
        servers["github"] = {
            "transport": "streamable_http",
            "url": github_url,
            "headers": {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
        }
        print(f"GitHub repository tools: {'read/write' if github_write_enabled else 'read-only'}")

    client = MultiServerMCPClient(servers)
    
    # Open this MCP session, and remember that I need to close it later
    async with AsyncExitStack() as stack:
        tools = []
        for name in servers:
            # Open a session to that MCP server
            session = await stack.enter_async_context(client.session(name))
            tools += await load_mcp_tools(session)
        print(f"Loaded {len(tools)} tools from: {', '.join(servers)}")

        # creat agent
        model = ChatOllama(model="gemma4:12b", num_ctx=16384)
        agent = create_agent(model=model, tools=tools)

    # invoke agent
        user_input = input("You: ").strip()
        result = await agent.ainvoke({"messages": [HumanMessage(content=user_input)]})

        # Show which tools the agent decided to use.
        for message in result["messages"]:
            for call in getattr(message, "tool_calls", []):
                print(f"  -> used tool: {call['name']}")

        print(f"Agent: {result['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(main())
