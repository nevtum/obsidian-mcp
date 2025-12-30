# Obsidian MCP: Knowledge Base API

## Overview

Obsidian MCP is a read-only API designed to interact with markdown notes stored in an Obsidian vault. Built for agentic AI applications, this Python-based service provides advanced note discovery, searching, and linking capabilities.

## Features

- 🔍 Full-text note search (exact and fuzzy matching)
- 🔗 Link extraction and discovery between notes
- 📊 Relevance-based note recommendations
- 🚀 Fast and efficient knowledge graph traversal

## Technologies

- Python
- FastAPI
- Uvicorn
- YAML (for frontmatter parsing)
- Docker

## Prerequisites

- Docker
- An Obsidian vault with markdown notes

## Docker Installation and Usage

### Build the Docker Image

```bash
make build
```

### Running the API in Docker

#### Default Vault Path
By default, the Docker container will use the vault path specified in your home directory:
```bash
make run
```
This mounts `~/Documents/vault` as the default Obsidian vault.

#### Custom Vault Path
To use a custom Obsidian vault path, set the `OBSIDIAN_VAULT_PATH` environment variable:

```bash
# macOS/Linux
OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault make run

# Windows PowerShell
$env:OBSIDIAN_VAULT_PATH="/path/to/your/obsidian/vault"; make run
```

### Stopping the Docker Container

```bash
make stop
```

### Cleaning Up Docker Resources

```bash
make clean
```

## Manual Installation (Alternative to Docker)

### Prerequisites for Manual Setup

- Python 3.9+
- `uv` (Universal Python Package Manager)

### Manual Installation Steps

1. Install `uv` (if not already installed):
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/obsidian-mcp.git
cd obsidian-mcp
```

3. Create and activate a virtual environment:
```bash
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate (use .venv\Scripts\activate on Windows)
```

4. Install dependencies:
```bash
uv pip install -r requirements.txt
```

5. Set the vault path:
```bash
# Create a .env file
echo "OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault" > .env
```

6. Run the server:
```bash
python main.py
```

## API Endpoints

- `GET /`: List all note slugs
- `GET /search`: Search notes (with optional exact matching)
- `GET /{slug}/links`: Find links in a specific note
- `GET /{slug}/relevant`: Find contextually related notes
- `POST /details`: Batch retrieve note details

## Example Queries

1. Search notes:
```bash
curl "http://localhost:8000/search?q=python&exact=false"
```

2. Find note links:
```bash
curl "http://localhost:8000/notes/machine-learning/links"
```

3. Find relevant notes:
```bash
curl "http://localhost:8000/notes/data-science/relevant?max_hops=3&char_limit=150"
```
