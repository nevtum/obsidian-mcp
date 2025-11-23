import pytest

from obsidian_api.note import Note
from obsidian_api.vault import ObsidianVault


@pytest.fixture
def vault():
    vault_instance = ObsidianVault(directory="test_directory")
    vault_instance.notes = {
        "note1": Note(
            slug="note1",
            filename="note1.md",
            text="This is the first note content.",
        ),
        "note2": Note(
            slug="note2",
            filename="note2.md",
            text="This is the second note with different content.",
        ),
        "note3": Note(
            slug="note3",
            filename="note3.md",
            text="Another note that talks about different things.",
        ),
    }
    vault_instance.build_index()  # Build index for searching
    return vault_instance


def test_search_notes_exact_match(vault):
    result = vault.search_notes("first")
    assert result == [{"frontmatter": {}, "slug": "note1"}], (
        "Should return 'note1' for exact match on 'first'."
    )

    result = vault.search_notes("second")

    assert result == [{"frontmatter": {}, "slug": "note2"}], (
        "Should return 'note2' for exact match on 'second'."
    )

    result = vault.search_notes("different")
    assert result == [
        {"frontmatter": {}, "slug": "note2"},
        {"frontmatter": {}, "slug": "note3"},
    ], "Should return 'note2' and 'note3' for exact match on 'different'."


def test_search_notes_no_match(vault):
    result = vault.search_notes("nonexistent")
    assert result == [], "Should return an empty list for non-existent word search."


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
