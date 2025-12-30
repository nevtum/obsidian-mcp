FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

WORKDIR /app
COPY . /app

RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

# Set default environment variables
ENV OBSIDIAN_VAULT_PATH=/vault

# Expose port
EXPOSE 8000

# Set entrypoint using uv run
CMD ["uv", "run", "main.py"]
