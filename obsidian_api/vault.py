import os
from collections import deque

from obsidian_api.exceptions import DuplicateSlugDetected, NoteMissingException
from obsidian_api.note import Note


class ObsidianVault:
    def __init__(self, directory):
        self.directory = directory
        self.notes = {}
        self.load_notes()  # Load notes from the directory

    def list_note_slugs(self):
        return list(self.notes.keys())

    def find_relevant_notes(self, slug, max_hops=2, char_limit=100):
        queue = deque([(slug, 0)])
        visited = set()
        relevant_notes = []

        while queue:
            current_slug, current_hop = queue.popleft()

            if current_slug in visited:
                continue

            visited.add(current_slug)

            if current_hop <= max_hops:
                current_note = self.fetch_note_by_slug(current_slug)

                if current_hop > 0:
                    relevant_notes.append(
                        {
                            "filename": current_note.filename,
                            "contents_summary": current_note.content[:char_limit],
                            "distance": current_hop,
                        }
                    )

                for link in current_note.extract_links():
                    if link in self.notes:
                        queue.append((link, current_hop + 1))

        return relevant_notes

    def find_ancestors(self, slug, max_hops=2, char_limit=100):
        raise NotImplementedError("find_ancestors method is not implemented yet.")

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
        if slug in self.notes:
            # TODO: unit test this logic
            raise DuplicateSlugDetected(slug)
        self.notes[slug] = Note(slug=slug, filename=filepath, content=content)

    def watch_changes(self):
        """A mock implementation that simulates change detection."""
        return True
