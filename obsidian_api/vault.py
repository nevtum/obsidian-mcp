from obsidian_api.exceptions import NoteMissingException


from obsidian_api.note import Note


class ObsidianVault:
    def __init__(self, directory):
        self.directory = directory

    def find_relevant_notes(self, start_slug, max_hops=2, char_limit=100):
        """A mock implementation that simulates finding relevant notes."""
        return [
            {
                "filename": "note1.md",
                "contents_summary": "Summary of note1",
                "distance": 1,
            },
            {
                "filename": "note2.md",
                "contents_summary": "Summary of note2",
                "distance": 2,
            },
        ]

    def __init__(self, directory):
        self.notes = {
            "note1.md": Note(filename="note1.md", content="Content of note 1."),
            "note2.md": Note(filename="note2.md", content="Content of note 2."),
        }

    def fetch_note_by_slug(self, slug):
        if slug not in self.notes:
            raise NoteMissingException(f"No note found with slug: {slug}")
        return self.notes[slug]

    def watch_changes(self):
        """A mock implementation that simulates change detection."""
        return True
