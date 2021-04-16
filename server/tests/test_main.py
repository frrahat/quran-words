from fastapi.testclient import TestClient

from server.main import app
from server.config import CONFIG

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_list_word_80_percent_levels():
    response = client.get("/words-80-percent/levels")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['pagination'] == {
        'previous': None,
        'next': f"{CONFIG.BASE_URL}/words-80-percent/levels?offset=10&pagesize=10",
    }


def test_list_word_80_percent_levels_with_pagesize_param():
    response = client.get("/words-80-percent/levels?offset=4&pagesize=6")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json['data']) == 6
    assert response_json['data'][0]['num'] == 5

    assert response_json['pagination'] == {
        'previous': f"{CONFIG.BASE_URL}/words-80-percent/levels?offset=0&pagesize=4",
        'next': f"{CONFIG.BASE_URL}/words-80-percent/levels?offset=10&pagesize=6",
    }


def test_list_word_80_percent_words():
    response = client.get("/words-80-percent/words")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['pagination'] == {
        'previous': None,
        'next': f"{CONFIG.BASE_URL}/words-80-percent/words?offset=10&pagesize=10",
    }


def test_list_word_80_percent_words_with_pagesize_param():
    response = client.get("/words-80-percent/words?offset=7&pagesize=12")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json['data']) == 12
    assert response_json['data'][0]['serial'] == 8

    assert response_json['pagination'] == {
        'previous': f"{CONFIG.BASE_URL}/words-80-percent/words?offset=0&pagesize=7",
        'next': f"{CONFIG.BASE_URL}/words-80-percent/words?offset=19&pagesize=12",
    }


def test_list_verses_by_surah():
    response = client.get("/verses/sura/2")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['pagination'] == {
        'previous': None,
        'next': f"{CONFIG.BASE_URL}/verses/sura/2?offset=10&pagesize=10",
    }


def test_list_verses_by_surah_with_pagesize_param():
    response = client.get("/verses/sura/2?offset=14&pagesize=19")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json['data']) == 19
    assert response_json['data'][0]['ayah'] == 15

    assert response_json['pagination'] == {
        'previous': f"{CONFIG.BASE_URL}/verses/sura/2?offset=0&pagesize=14",
        'next': f"{CONFIG.BASE_URL}/verses/sura/2?offset=33&pagesize=19",
    }


def test_get_verse():
    response = client.get("/verses/sura/2/ayah/282")
    assert response.status_code == 200


def test_get_corpus():
    response = client.get("/corpus/sura/2/ayah/282")
    assert response.status_code == 200
