import pytest
from obsidian_api import Note, ObsidianVault


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
    return ObsidianVault(directory="test_data")


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


def test_change_detection(vault):
    # Assuming `watch_changes` method is implemented in ObsidianVault
    assert vault.watch_changes() is True


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
