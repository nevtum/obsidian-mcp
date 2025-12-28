from os import getenv

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse

from obsidian_api.exceptions import NoteMissingException
from obsidian_api.vault import ObsidianVault

from .schema import (
    FindNoteLinksResponse,
    FindRelevantNotesResponse,
    GetNoteResponse,
    ListNoteSlugsResponse,
)

router = APIRouter()


def get_vault():
    path = getenv("OBSIDIAN_VAULT_PATH", "tests/test_data")
    return ObsidianVault(directory=path)


@router.get("/")
async def index():
    return RedirectResponse("/docs")


@router.get("/notes/{slug}/content", response_model=str)
async def read_note_content(slug: str, vault: ObsidianVault = Depends(get_vault)):
    """
    Retrieve the full text content of a specific note by its slug.

    This endpoint fetches the raw text content of a note in an Obsidian vault.

    Parameters:
    -----------
    slug : str
        The unique identifier (slug) of the note to retrieve.
        This is typically derived from the note's filename without the extension.
        Example: For a note named "Machine Learning Basics.md", the slug would be "machine-learning-basics"

    Responses:
    ----------
    200 OK:
        Returns the full text content of the note as plain text.
        Content-Type: text/plain

    404 Not Found:
        Raised if no note exists with the provided slug.
        This can happen if:
        - The slug is misspelled
        - The note has been deleted
        - The note does not exist in the vault

    Example Usage:
    --------------
    Request: GET /notes/machine-learning-basics/content
    Response:
        "# Machine Learning Basics

        Machine learning is a method of data analysis that..."

    Raises:
    -------
    HTTPException
        A 404 error is raised if the note cannot be found in the vault.
    """
    try:
        note = vault.fetch_note_by_slug(slug)
        return PlainTextResponse(note.content)
    except NoteMissingException as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.get("/notes/{slug}/links", response_model=FindNoteLinksResponse)
async def find_links(slug: str, vault: ObsidianVault = Depends(get_vault)):
    """
    Extract and retrieve all links present within a specific note.

    This endpoint discovers the interconnected network of links
    in a given note, which is crucial for understanding note relationships in an
    Obsidian vault.

    Parameters:
    -----------
    slug : str
        The unique identifier (slug) of the note to extract links from.
        This is typically derived from the note's filename without the extension.
        Example: For a note named "Machine Learning Basics.md", the slug would be "machine-learning-basics"

    Responses:
    ----------
    200 OK:
        Returns a structured response containing:
        - params: The input parameters used for the request
        - links: A list of all links found within the note

    Response Schema:
    ---------------
    {
        "params": {
            "slug": str  # The input note slug
        },
        "links": [
            # List of links extracted from the note
            # Each link could be a direct wiki-style link or markdown link
        ]
    }

    Example Usage:
    --------------
    Request: GET /notes/machine-learning-basics/links
    Response:
    {
        "params": {"slug": "machine-learning-basics"},
        "links": [
            "neural-networks",
            "deep-learning",
            "data-science"
        ]
    }

    Notes:
    ------
    - Links are extracted directly from the note's content
    - Supports various link formats typical in Markdown and Obsidian
    - Does not validate if linked notes actually exist in the vault

    Raises:
    -------
    HTTPException
        A 404 error is raised if the note cannot be found in the vault.
    """
    note = vault.fetch_note_by_slug(slug)
    links = note.extract_links()
    return {
        "params": {
            "slug": slug,
        },
        "links": links,
    }


@router.get("/notes/{slug}/relevant", response_model=FindRelevantNotesResponse)
async def find_relevant_notes(
    slug: str,
    max_hops: int = 2,
    char_limit: int = 100,
    vault: ObsidianVault = Depends(get_vault),
):
    """
    Discover and retrieve notes that are closely related to a given note.

    This endpoint helps explore the interconnected knowledge network within a vault
    by finding notes that are contextually relevant to the specified note.

    Parameters:
    -----------
    slug : str
        The unique identifier (slug) of the reference note.
        This is typically derived from the note's filename without the extension.
        Example: For a note named "Machine Learning Basics.md", the slug would be "machine-learning-basics"

    max_hops : int, optional
        The maximum number of link "hops" to traverse when finding related notes.
        - Default is 2, meaning it will explore links up to two steps away from the original note
        - A higher value increases the breadth of related notes, but may slow down the search
        - A lower value provides more focused, immediate connections

    char_limit : int, optional
        Limits the number of characters returned for each relevant note's preview.
        - Default is 100 characters
        - Helps keep the response concise and manageable
        - Useful for quickly scanning related note summaries

    Responses:
    ----------
    200 OK:
        Returns a structured response containing:
        - params: The input parameters used for the request
        - results: A list of relevant notes with their details

    Response Schema:
    ---------------
    {
        "params": {
            "slug": str,           # The input reference note
            "max_hops": int,       # Number of link hops
            "char_limit": int      # Character preview limit
        },
        "results": [
            {
                "slug": str,        # Slug of the related note
                "preview": str,     # Short preview of the note's content
                # Other possible note metadata
            }
        ]
    }

    Example Usage:
    --------------
    Request: GET /notes/machine-learning/relevant?max_hops=3&char_limit=150
    Response:
    {
        "params": {
            "slug": "machine-learning",
            "max_hops": 3,
            "char_limit": 150
        },
        "results": [
            {
                "slug": "neural-networks",
                "preview": "Neural networks are a fundamental component of deep learning..."
            },
            {
                "slug": "data-science-techniques",
                "preview": "Exploring various approaches to solving complex data science challenges..."
            }
        ]
    }

    Notes:
    ------
    - The relevance is determined by direct and indirect links between notes
    - Results are not ranked by importance, but by connection proximity
    - The number and nature of results depend on your vault's link structure
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


@router.get("/notes/{slug}", response_model=GetNoteResponse)
async def get_note(slug: str, vault: ObsidianVault = Depends(get_vault)):
    try:
        note = vault.fetch_note_by_slug(slug)
        return {
            "results": note.as_json(),
        }
    except NoteMissingException:
        raise HTTPException(status_code=404, detail="Note not found")


@router.get("/notes", response_model=ListNoteSlugsResponse)
async def list_note_slugs(vault: ObsidianVault = Depends(get_vault)):
    return {"results": vault.list_note_slugs()}


@router.get("/search")
async def search_notes(
    q: str, exact: bool = False, vault: ObsidianVault = Depends(get_vault)
):
    """
    Search for notes across the vault using flexible search strategies.

    This endpoint allows searching through note contents using different matching approaches.

    Parameters:
    -----------
    q : str
        The search query string to find matching notes.
        - Can be a word, phrase, or partial content from a note
        - Search is case-insensitive
        - Supports searching across entire note contents

    exact : bool, optional
        Determines the search matching strategy.
        - When False (default): Performs a fuzzy, flexible search
          * Matches similar words and related content
          * More lenient, returns broader results
          * Good for finding notes with similar themes or partial matches

        - When True: Performs an exact, strict search
          * Requires precise matches of the search term
          * More restrictive, returns fewer, more precise results
          * Useful for finding specific content or quotes

    Responses:
    ----------
    200 OK:
        Returns a structured response with search results
        {
            "results": [
                "note-slug-1",
                "note-slug-2",
                ...
            ]
        }

    Example Usage:
    --------------
    1. Fuzzy Search (default):
       Request: GET /search?q=machine learning
       Returns notes containing similar or related terms

    2. Exact Search:
       Request: GET /search?q=machine learning&exact=true
       Returns only notes with exact phrase match

    Notes:
    ------
    - Search is performed across all notes in the vault
    - Results are returned as a list of note slugs
    - No guarantee of result order or ranking
    """
    return {"results": vault.search_notes(q) if exact else vault.fuzzy_search_notes(q)}
