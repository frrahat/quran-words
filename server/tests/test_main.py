from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_list_word_80_percent_levels():
    response = client.get("/words-80-percent/levels")
    assert response.status_code == 200


def test_list_word_80_percent_levels_with_pagesize_param():
    offset = 4
    pagesize = 6
    response = client.get(
        f"/words-80-percent/levels?offset={offset}&pagesize={pagesize}")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json['data']) == pagesize
    assert response_json['data'][0]['num'] == offset + 1


def test_list_word_80_percent_words():
    response = client.get("/words-80-percent/words")
    assert response.status_code == 200


def test_list_word_80_percent_words_with_pagesize_param():
    offset = 7
    pagesize = 12
    response = client.get(
        f"/words-80-percent/words?offset={offset}&pagesize={pagesize}")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json['data']) == pagesize
    assert response_json['data'][0]['serial'] == offset + 1


def test_list_verses_by_surah():
    response = client.get("/verses/sura/2")
    assert response.status_code == 200


def test_list_verses_by_surah_with_pagesize_param():
    offset = 14
    pagesize = 19
    response = client.get(
        f"/verses/sura/2?offset={offset}&pagesize={pagesize}")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json['data']) == pagesize
    assert response_json['data'][0]['ayah'] == offset + 1


def test_get_verse():
    response = client.get("/verses/sura/2/ayah/282")
    assert response.status_code == 200


def test_list_corpus():
    response = client.get("/corpus/sura/2/ayah/282")
    assert response.status_code == 200
