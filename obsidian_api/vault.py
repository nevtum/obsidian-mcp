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
        for root, _, files in os.walk(self.directory):
            for filename in files:
                if filename.endswith(".md"):
                    self._load_note_file(os.path.join(root, filename))

    def _load_note_file(self, filepath):
        with open(filepath, "r") as file:
            content = file.read()
        slug = os.path.basename(filepath)[:-3]  # Remove the '.md' extension for slug
        print(f"Loaded note: {slug} from {filepath}")
        self.notes[slug] = Note(filename=filepath, content=content)

    def watch_changes(self):
        """A mock implementation that simulates change detection."""
        return True
