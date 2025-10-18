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

    def watch_changes(self):
        """A mock implementation that simulates change detection."""
        return True
