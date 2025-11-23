from os import getenv

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, RedirectResponse

from obsidian_api.exceptions import NoteMissingException
from obsidian_api.vault import ObsidianVault

router = APIRouter()


def get_vault():
    path = getenv("OBSIDIAN_VAULT_PATH", "tests/test_data")
    return ObsidianVault(directory=path)


@router.get("/")
async def index():
    return RedirectResponse("/docs")


@router.get("/notes/{slug}/content")
async def read_raw_note(slug: str, vault: ObsidianVault = Depends(get_vault)):
    try:
        note = vault.fetch_note_by_slug(slug)
        return PlainTextResponse(note.content)
    except NoteMissingException:
        raise HTTPException(status_code=404, detail="Note not found")


@router.get("/notes/{slug}/links")
async def find_links(slug: str, vault: ObsidianVault = Depends(get_vault)):
    note = vault.fetch_note_by_slug(slug)
    links = note.extract_links()  # Assumes Note class has this method
    return {
        "params": {
            "slug": slug,
        },
        "links": links,
    }


@router.get("/notes/{slug}/relevant")
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


@router.get("/notes/{slug}")
async def read_note(slug: str, vault: ObsidianVault = Depends(get_vault)):
    try:
        note = vault.fetch_note_by_slug(slug)
        return {
            "results": note.as_json(),
        }
    except NoteMissingException:
        raise HTTPException(status_code=404, detail="Note not found")


@router.get("/notes")
async def list_note_slugs(vault: ObsidianVault = Depends(get_vault)):
    return {"results": vault.list_note_slugs()}
