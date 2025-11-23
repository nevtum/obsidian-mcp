import pytest
from fastapi.testclient import TestClient

from obsidian_api.api import app

client = TestClient(app)

# TODO: test other endpoints


def test_get_note_success():
    response = client.get("/notes/index")
    assert response.status_code == 200
    assert response.json() == {
        "results": {
            "slug": "index",
            "content": "This is an index file",
            "frontmatter": {"title": "My index"},
        },
    }


def test_read_note_not_found():
    response = client.get("/notes/non_existent_note")

    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


if __name__ == "__main__":
    pytest.main([__file__, "-sv"])
