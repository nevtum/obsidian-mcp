import pytest

from obsidian_api.exceptions import NoteMissingException
from obsidian_api.note import Note
from obsidian_api.vault import ObsidianVault

FRONTMATTER1 = """---
title: About Me
tags: [personal, introduction]
---
"""

FRONTMATTER2 = """---
title: About Me
tags:
  - personal
  - introduction
---
"""


@pytest.fixture
def sample_note():
    content = "This is a note about myself. You can find more in [[projects]] and [[hobbies]]."
    return Note(
        slug="about-me",
        filename="test_data/about-me.md",
        text=f"{FRONTMATTER1}\n{content}",
    )


@pytest.fixture
def vault():
    return ObsidianVault(directory="tests/test_data")


@pytest.mark.parametrize(
    "slug, filename, frontmatter",
    [
        ("about-me", "test_data/about-me.md", FRONTMATTER1),
        ("index", "vault/index.md", FRONTMATTER2),
    ],
)
def test_note_initialization(slug, filename, frontmatter):
    content = "This is a note about myself. You can find more in [[projects]] and [[hobbies]]."
    text = f"{frontmatter}\n{content}"
    note = Note(
        slug=slug,
        filename=filename,
        text=text,
    )
    assert note.text == text
    assert note.content == content
    assert note.frontmatter == {
        "title": "About Me",
        "tags": ["personal", "introduction"],
    }
    assert note.slug == slug
    assert note.filepath == filename
    assert note.filename == filename.split("/")[-1]


def test_extract_links(sample_note):
    links = sample_note.extract_links()
    assert links == ["projects", "hobbies"]


def test_find_relevant_notes(vault):
    relevant_notes = vault.find_relevant_notes(slug="note2", max_hops=2, char_limit=100)
    assert isinstance(relevant_notes, list)
    assert all("filename" in note for note in relevant_notes)
    assert all("content_summary" in note for note in relevant_notes)
    assert all("distance" in note for note in relevant_notes)


def test_fetch_note_by_slug(vault):
    with pytest.raises(NoteMissingException):  # Ensure NoteMissingException is raised
        vault.fetch_note_by_slug(
            "non_existent_slug"
        )  # Attempt to fetch a non-existent note


@pytest.mark.parametrize(
    "slug, expected_content, expected_frontmatter, expected_links",
    [
        (
            "note1",
            "This is a sample note for testing purposes.",
            {"title": "Note 1", "tags": ["sample", "test"]},
            [],
        ),
        (
            "note2",
            "This is another sample note for testing purposes.\nHere's a link to [[note1]] and to [[note3]].",
            {"title": "Note 2", "tags": ["sample", "test"]},
            ["note1", "note3"],
        ),
        (
            "note3",
            "This is a third sample note for testing purposes.",
            {"title": "Note 3", "tags": ["sample", "test"]},
            [],
        ),
    ],
)
def test_fetch_note_contents(
    vault, slug, expected_content, expected_frontmatter, expected_links
):
    note = vault.fetch_note_by_slug(slug)
    assert note.content == expected_content
    assert note.frontmatter == expected_frontmatter
    assert note.extract_links() == expected_links


def test_change_detection(vault):
    # Assuming `watch_changes` method is implemented in ObsidianVault
    assert vault.watch_changes() is True


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
