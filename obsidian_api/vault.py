import logging
import os
import re
from collections import defaultdict, deque
from difflib import get_close_matches

from obsidian_api.exceptions import DuplicateSlugDetected, NoteMissingException
from obsidian_api.note import Note

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ObsidianVault:
    def __init__(self, directory):
        self.directory = directory
        self.notes = {}
        self.load_notes()
        self.build_index()

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
                            "content_summary": current_note.content[:char_limit],
                            "distance": current_hop,
                        }
                    )

                for link in current_note.extract_links():
                    if link in self.notes:
                        queue.append((link, current_hop + 1))

        return relevant_notes

    def search_notes(self, query: str):
        return self.index.get(query, [])

    def fuzzy_search_notes(self, query: str):
        slugs = set()
        for word in get_close_matches(query, self.index.keys()):
            for slug in self.index[word]:
                slugs.add(slug)

        return list(slugs)

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

    def build_index(self):
        self.index = defaultdict(list)
        for slug, note in self.notes.items():
            words = set(re.findall(r"\w+", note.content.lower()))
            for word in words:
                self.index[word].append(slug)

        logger.info(f"Index built successfully! {len(self.index)} total words indexed.")

    def _load_note_file(self, filepath):
        slug = os.path.basename(filepath)[:-3]  # Remove the '.md' extension for slug
        if slug in self.notes:
            # TODO: unit test this logic
            raise DuplicateSlugDetected(slug)

        with open(filepath, "r") as file:
            text = file.read()
            logger.info(f"Loaded note: {slug} from {filepath}")
            self.notes[slug] = Note(slug=slug, filename=filepath, text=text)

    def watch_changes(self):
        """A mock implementation that simulates change detection."""
        return True
