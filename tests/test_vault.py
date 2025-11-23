import pytest

from obsidian_api.exceptions import NoteMissingException
from obsidian_api.note import Note
from obsidian_api.vault import ObsidianVault


@pytest.fixture
def vault():
    """Fixture to create a test ObsidianVault with mock notes."""
    vault = ObsidianVault("/test/path/to/notes")

    # Mock notes for testing
    vault.notes = {
        "note1": Note(
            "note1",
            "note1.md",
            "This is the first note. It links to [[note2]] and [[note3]].",
        ),
        "note2": Note(
            "note2",
            "note2.md",
            "This is the second note. It links to [[note3]] and [[note4]].",
        ),
        "note3": Note(
            "note3", "note3.md", "This is the third note. It links to [[phantom-note]]."
        ),
        "note4": Note("note4", "note4.md", "This is the fourth note. No links."),
    }
    return vault


# TODO: test for duplicate slug detected


def test_find_relevant_notes_within_hops(vault):
    results = vault.find_relevant_notes("note1", max_hops=2, char_limit=18)

    assert results == [
        {
            "slug": "note2",
            "content_summary": "This is the second",
            "frontmatter": {},
            "distance": 1,
        },
        {
            "slug": "note3",
            "content_summary": "This is the third ",
            "frontmatter": {},
            "distance": 1,
        },
        {
            "slug": "note4",
            "content_summary": "This is the fourth",
            "frontmatter": {},
            "distance": 2,
        },
    ]


def test_find_relevant_notes_no_hops(vault):
    results = vault.find_relevant_notes("note1", max_hops=0, char_limit=50)

    assert results == []


def test_find_relevant_notes_nonexistent_note(vault):
    with pytest.raises(NoteMissingException):
        vault.find_relevant_notes("nonexistent_note", max_hops=2, char_limit=50)


def test_find_relevant_notes_with_no_links(vault):
    results = vault.find_relevant_notes("note3", max_hops=2, char_limit=50)

    assert results == []


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
