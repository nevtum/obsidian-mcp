from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi import Depends
from obsidian_api.vault import ObsidianVault
from obsidian_api.exceptions import NoteMissingException

app = FastAPI()


def get_vault() -> ObsidianVault:
    return ObsidianVault(directory="tests/test_data")  # Specify your vault path


@app.get("/")
async def index():
    return RedirectResponse("/docs")


@app.get("/notes/{slug}")
async def read_note(slug: str, vault: ObsidianVault = Depends(get_vault)):
    try:
        note = vault.fetch_note_by_slug(slug)
        return note.as_json()
    except NoteMissingException:
        raise HTTPException(status_code=404, detail="Note not found")


@app.get("/notes/{slug}/content")
async def read_raw_note(slug: str, vault: ObsidianVault = Depends(get_vault)):
    try:
        note = vault.fetch_note_by_slug(slug)
        return PlainTextResponse(note.content)
    except NoteMissingException:
        raise HTTPException(status_code=404, detail="Note not found")


@app.get("/notes/{slug}/links")
async def find_links(slug: str, vault: ObsidianVault = Depends(get_vault)):
    note = vault.fetch_note_by_slug(slug)
    links = note.extract_links()  # Assumes Note class has this method
    return {"links": links}


@app.get("/notes/{slug}/relevant")
async def find_relevant_notes(
    slug: str,
    max_hops: int = 2,
    char_limit: int = 100,
    vault: ObsidianVault = Depends(get_vault),
):
    relevant_notes = vault.find_relevant_notes(slug, max_hops, char_limit)
    return relevant_notes


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
