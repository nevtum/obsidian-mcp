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
    try:
        note = vault.fetch_note_by_slug(slug)
        return PlainTextResponse(note.content)
    except NoteMissingException as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.get("/notes/{slug}/links", response_model=FindNoteLinksResponse)
async def find_links(slug: str, vault: ObsidianVault = Depends(get_vault)):
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
    return {"results": vault.search_notes(q) if exact else vault.fuzzy_search_notes(q)}
