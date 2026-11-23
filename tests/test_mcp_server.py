import string
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

SERVER = (
    Path(__file__).resolve().parents[1] / "src" / "workshop-21" / "08-mcp" / "server.py"
)


class MCPServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_tools(self):
        async with Client(PythonStdioTransport(SERVER)) as client:
            tools = await client.list_tools()
            self.assertEqual(
                {tool.name for tool in tools}, {"generate_password", "get_time"}
            )

            characters = set(string.ascii_letters + string.digits + "!@#$%^&*()-_+=")
            for arguments, expected_length in [
                ({}, 16),
                ({"length": 8}, 8),
                ({"length": 128}, 128),
            ]:
                result = await client.call_tool("generate_password", arguments)
                password = result.content[0].text
                self.assertEqual(len(password), expected_length)
                self.assertTrue(set(password) <= characters)

            for length in (7, 129):
                result = await client.call_tool(
                    "generate_password", {"length": length}, raise_on_error=False
                )
                self.assertTrue(result.is_error)
                self.assertIn("between 8 and 128", result.content[0].text)

            before = datetime.now(timezone.utc)
            result = await client.call_tool("get_time")
            after = datetime.now(timezone.utc)
            current_time = datetime.fromisoformat(result.content[0].text)
            self.assertEqual(current_time.utcoffset(), timezone.utc.utcoffset(None))
            self.assertTrue(before <= current_time <= after)


class MCPClientTests(unittest.TestCase):
    def run_client(self, *args):
        return subprocess.run(
            [sys.executable, str(SERVER.with_name("client.py")), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=45,
        )

    def test_password_and_time(self):
        password = self.run_client("generate_password", "--length", "20")
        self.assertEqual(password.returncode, 0, password.stderr)
        self.assertEqual(len(password.stdout.strip()), 20)

        before = datetime.now(timezone.utc)
        time = self.run_client("get_time")
        after = datetime.now(timezone.utc)
        self.assertEqual(time.returncode, 0, time.stderr)
        self.assertTrue(before <= datetime.fromisoformat(time.stdout.strip()) <= after)

    def test_invalid_length(self):
        result = self.run_client("generate_password", "--length", "7")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("between 8 and 128", result.stderr)


if __name__ == "__main__":
    unittest.main()
