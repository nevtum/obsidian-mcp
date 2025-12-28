from dotenv import load_dotenv
from fastmcp import FastMCP

from obsidian_api.api import app


def main():
    _ = load_dotenv()

    mcp = FastMCP.from_fastapi(app)
    mcp.run(transport="http", port=8000)


if __name__ == "__main__":
    main()
