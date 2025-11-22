import uvicorn
from dotenv import load_dotenv

from obsidian_api.api import app


def main():
    _ = load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
