import pytest
from fastapi.testclient import TestClient
from obsidian_api.api import app

client = TestClient(app)

# TODO: add test for get note success


def test_read_note_not_found():
    """Test reading a note that does not exist."""
    response = client.get("/notes/non_existent_note")

    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
