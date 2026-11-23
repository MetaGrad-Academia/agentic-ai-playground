import argparse
import asyncio
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
from fastmcp.exceptions import ToolError


async def call_tool(name: str, arguments: dict[str, int]) -> str:
    server = Path(__file__).with_name("server.py")
    async with Client(PythonStdioTransport(server)) as client:
        result = await client.call_tool(name, arguments)
        if not isinstance(result.data, str):
            raise RuntimeError(f"Unexpected response from {name}: expected text")
        return result.data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Call the password and time MCP server."
    )
    commands = parser.add_subparsers(dest="tool", required=True)
    password = commands.add_parser("generate_password", help="Generate a password")
    password.add_argument(
        "--length", type=int, default=16, help="Password length (8-128)"
    )
    commands.add_parser("get_time", help="Get the current UTC time")
    args = parser.parse_args()

    arguments = {"length": args.length} if args.tool == "generate_password" else {}
    try:
        result = asyncio.run(call_tool(args.tool, arguments))
    except ToolError as error:
        parser.exit(1, f"Tool error: {error}\n")
    print(result)


if __name__ == "__main__":
    main()
