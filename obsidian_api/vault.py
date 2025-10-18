import os
from obsidian_api.exceptions import NoteMissingException


from obsidian_api.note import Note


class ObsidianVault:
    def __init__(self, directory):
        self.directory = directory
        self.notes = {}
        self.load_notes()  # Load notes from the directory

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

    def fetch_note_by_slug(self, slug):
        if slug not in self.notes:
            raise NoteMissingException(f"No note found with slug: {slug}")
        return self.notes[slug]

    def load_notes(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".md"):
                with open(os.path.join(self.directory, filename), "r") as file:
                    content = file.read()
                # TODO: store the globally unique slug, not the filename
                self.notes[filename] = Note(filename=filename, content=content)

    # This part should be removed from here since it belongs in fetch_note_by_slug

    def watch_changes(self):
        """A mock implementation that simulates change detection."""
        return True
