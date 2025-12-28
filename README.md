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
- Watchdog (for file system monitoring)
- YAML (for frontmatter parsing)

## Prerequisites

- Python 3.9+
- `uv` (Universal Python Package Manager)
- An Obsidian vault with markdown notes

## Installation

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

## Configuration

Create a `.env` file in the project root with:
```
OBSIDIAN_VAULT_PATH=/path/to/your/obsidian/vault
```

## Running the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

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
