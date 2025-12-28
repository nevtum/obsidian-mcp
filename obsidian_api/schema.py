from pydantic import BaseModel


class NoteDetails(BaseModel):
    slug: str
    content: str
    frontmatter: dict


class GetNoteResponse(BaseModel):
    results: NoteDetails


class FindLinksParams(BaseModel):
    slug: str


class FindNoteLinksResponse(BaseModel):
    params: FindLinksParams
    links: list[str]


class FindRelevantNotesParams(BaseModel):
    slug: str
    max_hops: int
    char_limit: int


class RelevantNotesItem(BaseModel):
    slug: str
    content_summary: str
    frontmatter: dict
    distance: int


class FindRelevantNotesResponse(BaseModel):
    params: FindRelevantNotesParams
    results: list[RelevantNotesItem]


class ListNoteSlugsResponse(BaseModel):
    results: list[str]


class SearchNotesParams(BaseModel):
    query: str
    exact: bool


class SearchNotesItem(BaseModel):
    slug: str
    frontmatter: dict


class SearchNotesResponse(BaseModel):
    params: SearchNotesParams
    results: list[SearchNotesItem]
