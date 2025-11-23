import unittest

from obsidian_api.note import Note
from obsidian_api.vault import ObsidianVault


class TestObsidianVault(unittest.TestCase):
    def setUp(self):
        self.vault = ObsidianVault(directory="test_directory")
        self.vault.notes = {
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
        self.vault.build_index()  # Build index for searching

    def test_search_notes_exact_match(self):
        result = self.vault.search_notes("first")
        self.assertIn(
            "note1", result, "Should return 'note1' for exact match on 'first'."
        )

        result = self.vault.search_notes("second")
        self.assertIn(
            "note2", result, "Should return 'note2' for exact match on 'second'."
        )

        result = self.vault.search_notes("different")
        self.assertIn(
            "note2", result, "Should return 'note2' for exact match on 'different'."
        )
        self.assertIn(
            "note3", result, "Should return 'note3' for exact match on 'different'."
        )

    def test_search_notes_no_match(self):
        result = self.vault.search_notes("nonexistent")
        self.assertEqual(
            result, [], "Should return an empty list for non-existent word search."
        )


if __name__ == "__main__":
    unittest.main()
