from textwrap import dedent

import pytest

from obsidian_api.exceptions import NoteMissingException
from obsidian_api.note import Note
from obsidian_api.vault import ObsidianVault


@pytest.fixture
def sample_note():
    content = """---
    title: About Me
    tags: [personal, introduction]
    ---

    This is a note about myself. You can find more in [[projects]] and [[hobbies]].
    """
    return Note(filename="test_data/about_me.md", content=content)


@pytest.fixture
def vault():
    return ObsidianVault(directory="tests/test_data")


def test_note_initialization(sample_note):
    assert sample_note.filename == "about_me.md"
    assert (
        sample_note.content
        == """---
    title: About Me
    tags: [personal, introduction]
    ---

    This is a note about myself. You can find more in [[projects]] and [[hobbies]].
    """
    )
    assert sample_note.frontmatter == {
        "title": "About Me",
        "tags": ["personal", "introduction"],
    }


def test_extract_links(sample_note):
    links = sample_note.extract_links()
    assert links == ["projects", "hobbies"]


def test_find_relevant_notes(vault):
    # Assuming `find_relevant_notes` method is implemented in ObsidianVault
    relevant_notes = vault.find_relevant_notes(
        start_slug="about_me.md", max_hops=2, char_limit=100
    )
    assert isinstance(relevant_notes, list)
    assert all("filename" in note for note in relevant_notes)
    assert all("contents_summary" in note for note in relevant_notes)
    assert all("distance" in note for note in relevant_notes)


def test_fetch_note_by_slug(vault):
    with pytest.raises(NoteMissingException):  # Ensure NoteMissingException is raised
        vault.fetch_note_by_slug(
            "non_existent_slug"
        )  # Attempt to fetch a non-existent note


@pytest.mark.parametrize(
    "slug, expected_content, expected_frontmatter",
    [
        (
            "note1",
            dedent("""---
title: Note 1
tags: [sample, test]
---

This is a sample note for testing purposes.
     """),
            {"title": "Note 1", "tags": ["sample", "test"]},
        ),
        (
            "note2",
            dedent("""---
title: Note 2
tags: [sample, test]
---

This is another sample note for testing purposes.
     """),
            {"title": "Note 2", "tags": ["sample", "test"]},
        ),
        (
            "note3",
            dedent("""---
title: Note 3
tags: [sample, test]
---

This is a third sample note for testing purposes.
     """),
            {"title": "Note 3", "tags": ["sample", "test"]},
        ),
    ],
)
def test_fetch_note_contents(vault, slug, expected_content, expected_frontmatter):
    note = vault.fetch_note_by_slug(slug)
    assert note.content == expected_content
    assert note.frontmatter == expected_frontmatter


def test_change_detection(vault):
    # Assuming `watch_changes` method is implemented in ObsidianVault
    assert vault.watch_changes() is True


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
