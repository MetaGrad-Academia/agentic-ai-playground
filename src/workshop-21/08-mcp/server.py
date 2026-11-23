import secrets
import string
from datetime import datetime, timezone

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

mcp = FastMCP("Password and Time")


@mcp.tool
def generate_password(length: int = 16) -> str:
    """Generate a random password of 8 to 128 characters."""
    if not 8 <= length <= 128:
        raise ToolError("Password length must be between 8 and 128 characters.")

    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_+="
    return "".join(secrets.choice(characters) for _ in range(length))


@mcp.tool
def get_time() -> str:
    """Return the current UTC date and time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    mcp.run(transport="stdio")
