from os import getenv
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse

from obsidian_api.exceptions import NoteMissingException
from obsidian_api.vault import ObsidianVault

from .schema import (
    FindNoteLinksResponse,
    FindRelevantNotesResponse,
    GetNoteResponse,
    ListNoteSlugsResponse,
    NoteDetails,
    SearchNotesResponse,
)

router = APIRouter()


def get_vault():
    path = getenv("OBSIDIAN_VAULT_PATH", "tests/test_data")
    return ObsidianVault(directory=path)


@router.get("/", response_model=ListNoteSlugsResponse)
async def list_note_slugs(vault: ObsidianVault = Depends(get_vault)):
    """
    Retrieve a comprehensive list of all note slugs in the vault.

    Provides an overview of all available notes by their unique identifiers.

    Returns:
    --------
    ListNoteSlugsResponse
        A collection of all note slugs in the vault.

    Response Structure:
    ------------------
    {
        "results": [str]  # List of all note slugs
    }

    Features:
    ---------
    - Returns all note slugs in the vault
    - Sorted alphabetically
    - Provides quick inventory of available notes

    Example:
    --------
    GET /notes
    Response: {
        "results": [
            "data-science",
            "machine-learning",
            "project-management",
            "weekly-review"
        ]
    }

    Use Cases:
    ----------
    - Generating note indexes
    - Building navigation menus
    - Exploring vault contents

    Notes:
    ------
    - Number of results depends on vault size
    - No additional filtering applied
    """
    return {"results": vault.list_note_slugs()}


@router.get("/search", response_model=SearchNotesResponse)
async def search_notes(
    q: str, exact: bool = False, vault: ObsidianVault = Depends(get_vault)
):
    """
    Search notes across the entire vault. Keep search query to a maximum of 2-3 words for better results.

    Discovers notes matching a specific search query with flexible matching options.

    Parameters:
    -----------
    q : str
        Search query to find matching notes.
        - Supports words, phrases, partial content
        - Case-insensitive
        - Searches entire note contents

    exact : bool, optional
        Search matching strategy.
        - False (default): Fuzzy search
          * Matches similar words and themes
          * Broader, more flexible results
        - True: Strict exact match
          * Requires precise search term
          * Narrow, precise results

    Returns:
    --------
    {
        "params": {
            "query": str,
            "exact": bool
        },
        "results": [
            {
                "slug": str,        # Matching note slug
                "frontmatter": dict # Note's metadata dictionary
            }
        ]
    }

    Search Modes:
    -------------
    1. Fuzzy Search (default):
       GET /search?q=data science
       Returns notes about data science, machine learning, etc.

    2. Exact Search:
       GET /search?q="neural networks"
       Returns only notes with exact phrase

    Examples:
    ---------
    GET /search?q=python
    Response: {
        "params": {
            "query": "python",
            "exact": false
        },
        "results": [
            {
                "slug": "python-basics",
                "frontmatter": {
                    "tags": ["programming", "tutorial"],
                    "difficulty": "beginner"
                }
            },
            {
                "slug": "data-science-python",
                "frontmatter": {
                    "tags": ["data-science", "programming"],
                    "category": "analysis"
                }
            }
        ]
    }
    """
    return {
        "params": {
            "query": q,
            "exact": exact,
        },
        "results": vault.search_notes(q) if exact else vault.fuzzy_search_notes(q),
    }


@router.get("/{slug}/content", response_model=str)
async def read_raw_note_content(slug: str, vault: ObsidianVault = Depends(get_vault)):
    """
    Retrieve the complete text content of a specific note.

    Fetches the full raw text of a note using its unique slug identifier.

    Parameters:
    -----------
    slug : str
        Unique note identifier, typically the filename without extension.
        Converted to lowercase with hyphens.
        Example: "Machine Learning Basics.md" becomes "machine-learning-basics"

    Response:
    ---------
    Plain text content of the entire note.

    Errors:
    -------
    404 Error if note is not found, which can occur due to:
    - Incorrect slug spelling
    - Deleted note
    - Non-existent note in vault

    Example:
    --------
    GET /notes/machine-learning-basics/content
    → Returns full note text, including markdown formatting
    """
    try:
        note = vault.fetch_note_by_slug(slug)
        return PlainTextResponse(note.content)
    except NoteMissingException as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.get("/{slug}/links", response_model=FindNoteLinksResponse)
async def find_note_links(slug: str, vault: ObsidianVault = Depends(get_vault)):
    """
    Discover all links within a specific note.

    Extracts and lists all internal links found in a note's content.

    Parameters:
    -----------
    slug : str
        Unique note identifier (lowercase, hyphen-separated).
        Derived from filename without extension.
        Example: "machine-learning-basics"

    Returns:
    --------
    List of note links extracted from the document.

    Response:
    ---------
    {
        "params": {"slug": str},
        "links": [str]
    }

    Features:
    ---------
    - Finds wiki-style and markdown links
    - Links are extracted directly from note content
    - Does not verify link existence in vault

    Example:
    --------
    GET /notes/project-management/links
    Response: {
        "params": {"slug": "project-management"},
        "links": [
            "team-collaboration",
            "agile-methodology",
            "resource-planning"
        ]
    }

    Errors:
    -------
    404 Error if note is not found
    """
    note = vault.fetch_note_by_slug(slug)
    links = note.extract_links()
    return {
        "params": {
            "slug": slug,
        },
        "links": links,
    }


@router.get("/{slug}/relevant", response_model=FindRelevantNotesResponse)
async def find_relevant_notes(
    slug: str,
    max_hops: int = 2,
    char_limit: int = 100,
    vault: ObsidianVault = Depends(get_vault),
):
    """
    Discover connected and contextually related notes.

    Explores the knowledge network by finding notes linked to the specified note.

    Parameters:
    -----------
    slug : str
        Unique note identifier (lowercase, hyphen-separated).
        Example: "machine-learning-basics"

    max_hops : int, optional
        Maximum link traversal depth.
        - Default: 2 (explores connections up to two steps away)
        - Higher values: Broader but slower search
        - Lower values: More focused results

    char_limit : int, optional
        Maximum characters for note previews.
        - Default: 100 characters
        - Keeps results concise and scannable

    Returns:
    --------
    FindRelevantNotesResponse
        Collection of related notes with context.

    Response Structure:
    ------------------
    {
        "params": {
            "slug": str,
            "max_hops": int,
            "char_limit": int
        },
        "results": [
            {
                "slug": str,
                "content_summary": str,
                "distance": int
            }
        ]
    }

    Features:
    ---------
    - Finds notes through direct and indirect links
    - Connections based on vault's link structure
    - Results show proximity to original note

    Example:
    --------
    GET /notes/data-science/relevant?max_hops=3&char_limit=150
    Response: {
        "params": {
            "slug": "data-science",
            "max_hops": 3,
            "char_limit": 150
        },
        "results": [
            {
                "slug": "machine-learning",
                "content_summary": "Advanced techniques for predictive analysis...",
                "distance": 1
            }
        ]
    }

    Troubleshooting:
    ---------------
    - Ensure note exists in vault
    - Check note's internal linking
    - Adjust max_hops for broader/narrower results
    """
    relevant_notes = vault.find_relevant_notes(slug, max_hops, char_limit)
    return {
        "params": {
            "slug": slug,
            "max_hops": max_hops,
            "char_limit": char_limit,
        },
        "results": relevant_notes,
    }


@router.get("/{slug}", response_model=GetNoteResponse)
async def get_note_details(slug: str, vault: ObsidianVault = Depends(get_vault)):
    """
    Retrieve complete details of a specific note.

    Fetches comprehensive information about a note in the vault.

    Parameters:
    -----------
    slug : str
        Unique note identifier (lowercase, hyphen-separated).
        Example: "project-management-guide"

    Returns:
    --------
    GetNoteResponse
        Complete note details including content and metadata.

    Response Structure:
    ------------------
    {
        "results": {
            "slug": str,
            "content": str,
            "frontmatter": dict
        }
    }

    Features:
    ---------
    - Returns full note content
    - Includes frontmatter metadata
    - Provides comprehensive note information

    Example:
    --------
    GET /notes/data-science
    Response: {
        "results": {
            "slug": "data-science",
            "content": "# Data Science Overview...",
            "frontmatter": {
                "tags": ["analysis", "programming"],
                "created": "2023-01-15"
            }
        }
    }

    Errors:
    -------
    404 Error if note is not found
    """
    try:
        note = vault.fetch_note_by_slug(slug)
        return {
            "results": note.as_json(),
        }
    except NoteMissingException:
        raise HTTPException(status_code=404, detail="Note not found")


@router.post("/details", response_model=List[NoteDetails])
async def get_notes_batch(slugs: List[str], vault: ObsidianVault = Depends(get_vault)):
    """
    Retrieve complete details for multiple notes in a single request.

    Parameters:
    -----------
    slugs : List[str]
        List of unique note identifiers to fetch.

    Returns:
    --------
    List[NoteDetails]
        List of notes with their complete details.

    Errors:
    -------
    404 Error if any of the specified notes are not found.

    Example:
    --------
    POST /notes/batch
    Request body: ["data-science", "machine-learning"]
    Response: [
        {
            "slug": "data-science",
            "content": "# Data Science Overview...",
            "frontmatter": {...}
        },
        {
            "slug": "machine-learning",
            "content": "# Machine Learning Basics...",
            "frontmatter": {...}
        }
    ]
    """
    try:
        notes = []
        for slug in slugs:
            note = vault.fetch_note_by_slug(slug)
            notes.append(note.as_json())
        return notes
    except NoteMissingException as ex:
        raise HTTPException(status_code=404, detail=str(ex))
