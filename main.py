import logging

import uvicorn
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP

from obsidian_api.api import app

logging.basicConfig()

mcp = FastApiMCP(app, "Personal knowledge repository")
mcp.mount_http()


def main():
    _ = load_dotenv()

    uvicorn.run("obsidian_api.api:app", reload=True, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
