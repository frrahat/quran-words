from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_list_word_80_percent_levels():
    response = client.get("/words-80-percent/levels")
    assert response.status_code == 200


def test_list_word_80_percent_words():
    response = client.get("/words-80-percent/words")
    assert response.status_code == 200


def test_list_verses_by_surah():
    response = client.get("/verses/sura/2")
    assert response.status_code == 200


def test_get_verse():
    response = client.get("/verses/sura/2/ayah/282")
    assert response.status_code == 200


def test_get_corpus():
    response = client.get("/corpus/sura/2/ayah/282")
    assert response.status_code == 200
