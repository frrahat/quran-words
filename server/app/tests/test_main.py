import pytest
from fastapi.testclient import TestClient

from app.db.db_quran_arabic import QuranArabic
from app.db.db_quran_english import QuranEnglish
from app.main import app
from app.taraweeh_ayat import get_start_end_ayah_by_night

client = TestClient(app)


def _get_arabic_verse(sura, ayah):
    with QuranArabic.get_session() as session:
        return (
            session.query(QuranArabic)
            .filter(QuranArabic.sura_num == sura, QuranArabic.ayah_num == ayah)
            .first()
            .text
        )


def _get_english_translated_verse(sura, ayah):
    with QuranEnglish.get_session() as session:
        return (
            session.query(QuranEnglish)
            .filter(QuranEnglish.sura_num == sura, QuranEnglish.ayah_num == ayah)
            .first()
            .text
        )


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_read_app():
    response = client.get("/app")
    assert response.status_code == 200


def test_read_app_path():
    response = client.get("/app/something")
    assert response.status_code == 200


def test_read_words_path():
    response = client.get("/words/something")
    assert response.status_code == 200


def test_list_word_80_percent_levels():
    response = client.get("/api/words-80-percent/levels")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["pagination"] == {
        "previous": None,
        "next": "/api/words-80-percent/levels?offset=10&pagesize=10",
    }


def test_list_word_80_percent_levels_with_pagesize_param():
    response = client.get("/api/words-80-percent/levels?offset=4&pagesize=6")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["data"]) == 6
    assert response_json["data"][0]["num"] == 5

    assert response_json["pagination"] == {
        "previous": "/api/words-80-percent/levels?offset=0&pagesize=4",
        "next": "/api/words-80-percent/levels?offset=10&pagesize=6",
    }


def test_list_word_80_percent_words():
    response = client.get("/api/words-80-percent/words")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["pagination"] == {
        "previous": None,
        "next": "/api/words-80-percent/words?offset=10&pagesize=10",
    }


def test_list_word_80_percent_words_with_pagesize_param():
    response = client.get("/api/words-80-percent/words?offset=7&pagesize=12")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["data"]) == 12
    assert response_json["data"][0]["serial"] == 8

    assert response_json["pagination"] == {
        "previous": "/api/words-80-percent/words?offset=0&pagesize=7",
        "next": "/api/words-80-percent/words?offset=19&pagesize=12",
    }


def test_list_verses_by_surah():
    response = client.get("/api/verses/sura/2")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["pagination"] == {
        "previous": None,
        "next": "/api/verses/sura/2?offset=10&pagesize=10",
    }


def test_list_verses_by_surah_with_pagesize_param():
    response = client.get("/api/verses/sura/2?offset=14&pagesize=19")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["data"]) == 19
    assert response_json["data"][0]["ayah"] == 15

    assert response_json["pagination"] == {
        "previous": "/api/verses/sura/2?offset=0&pagesize=14",
        "next": "/api/verses/sura/2?offset=33&pagesize=19",
    }


def test_get_verse():
    response = client.get("/api/verses/sura/2/ayah/282")
    assert response.status_code == 200


def test_get_corpus():
    response = client.get("/api/corpus/sura/2/ayah/282")
    assert response.status_code == 200


def test_list_occurrences():
    root = "علم"
    response = client.get(f"/api/occurrences?root={root}")

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["data"]) == 10
    assert response_json["total"] == 728
    assert response_json["data"][0] == {
        "sura": 1,
        "ayah": 2,
        "verse": {
            "arabic": _get_arabic_verse(1, 2),
            "english": _get_english_translated_verse(1, 2),
            "words": [
                {"word_num": 1, "english": "All praises and thanks"},
                {"word_num": 2, "english": "(be) to Allah,"},
                {"word_num": 3, "english": "the Lord"},
                {"word_num": 4, "english": "of the universe"},
            ],
        },
        "word_nums": [4],
    }

    assert response_json["pagination"] == {
        "previous": None,
        "next": f"/api/occurrences?offset=10&pagesize=10&root={root}",
    }


def test_list_occurrences_with_root_and_lemma_param():
    root = "عبد"
    lemma = "عَبَدَ"
    response = client.get(f"/api/occurrences?root={root}&lemma={lemma}")

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["data"]) == 10
    assert response_json["total"] == 111
    assert response_json["data"][0] == {
        "sura": 1,
        "ayah": 5,
        "verse": {
            "arabic": _get_arabic_verse(1, 5),
            "english": _get_english_translated_verse(1, 5),
            "words": [
                {"word_num": 1, "english": "You Alone"},
                {"word_num": 2, "english": "we worship,"},
                {"word_num": 3, "english": "and You Alone"},
                {"word_num": 4, "english": "we ask for help."},
            ],
        },
        "word_nums": [2],
    }

    assert response_json["pagination"] == {
        "previous": None,
        "next": f"/api/occurrences?offset=10&pagesize=10&root={root}&lemma={lemma}",
    }


def test_list_occurrences_with_lemma_param():
    lemma = "مِن"
    response = client.get(f"/api/occurrences?lemma={lemma}")

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["data"]) == 10
    assert response_json["total"] == 2149
    assert response_json["data"][0] == {
        "sura": 2,
        "ayah": 4,
        "verse": {
            "arabic": _get_arabic_verse(2, 4),
            "english": _get_english_translated_verse(2, 4),
            "words": [
                {"word_num": 1, "english": "And those who"},
                {"word_num": 2, "english": "believe"},
                {"word_num": 3, "english": "in what"},
                {"word_num": 4, "english": "(is) sent down"},
                {"word_num": 5, "english": "to you"},
                {"word_num": 6, "english": "and what"},
                {"word_num": 7, "english": "was sent down"},
                {"word_num": 8, "english": "from"},
                {"word_num": 9, "english": "before you"},
                {"word_num": 10, "english": "and in the Hereafter"},
                {"word_num": 11, "english": "they"},
                {"word_num": 12, "english": "firmly believe."},
            ],
        },
        "word_nums": [8],
    }

    assert response_json["pagination"] == {
        "previous": None,
        "next": f"/api/occurrences?offset=10&pagesize=10&lemma={lemma}",
    }


def test_list_occurrences_with_pagesize_param():
    root = "علم"
    response = client.get(f"/api/occurrences?root={root}&offset=7&pagesize=8")

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["data"]) == 8
    assert response_json["total"] == 728
    assert response_json["data"][0] == {
        "sura": 2,
        "ayah": 32,
        "verse": {
            "arabic": _get_arabic_verse(2, 32),
            "english": _get_english_translated_verse(2, 32),
            "words": [
                {"word_num": 1, "english": "They said,"},
                {"word_num": 2, "english": '"Glory be to You!'},
                {"word_num": 3, "english": "No"},
                {"word_num": 4, "english": "knowledge"},
                {"word_num": 5, "english": "(is) for us"},
                {"word_num": 6, "english": "except"},
                {"word_num": 7, "english": "what"},
                {"word_num": 8, "english": "You have taught us."},
                {"word_num": 9, "english": "Indeed You!"},
                {"word_num": 10, "english": "You"},
                {"word_num": 11, "english": "(are) the All-Knowing,"},
                {"word_num": 12, "english": "the All-Wise."},
            ],
        },
        "word_nums": [4, 8, 11],
    }

    assert response_json["pagination"] == {
        "previous": f"/api/occurrences?offset=0&pagesize=7&root={root}",
        "next": f"/api/occurrences?offset=15&pagesize=8&root={root}",
    }


@pytest.mark.parametrize("taraweeh_night", range(1, 28))
def test_list_occurrences_with_taraweeh_night_param(taraweeh_night):
    root = "علم"
    response = client.get(
        f"/api/occurrences?root={root}&taraweeh_night={taraweeh_night}&page_size=1000"
    )

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json["data"]) >= 2

    sura_ayah_list = [
        (occurrence["sura"], occurrence["ayah"]) for occurrence in response_json["data"]
    ]
    sorted_sura_ayah_list = sorted(sura_ayah_list)

    upper_limit_ayah, lower_limit_ayah = get_start_end_ayah_by_night(taraweeh_night)
    assert sorted_sura_ayah_list[0] >= (upper_limit_ayah.sura, upper_limit_ayah.ayah)
    assert sorted_sura_ayah_list[-1] <= (lower_limit_ayah.sura, lower_limit_ayah.ayah)


def test_list_frequencies():
    response = client.get("/api/frequencies")

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json["data"]) == 10
    assert response_json["total"] == 4751
    assert response_json["data"][0] == {
        "lemma": "مِن",
        "root": "",
        "frequency": 3067,
    }

    assert response_json["pagination"] == {
        "previous": None,
        "next": "/api/frequencies?offset=10&pagesize=10",
    }


def test_list_frequencies_with_taraweeh_night_param():
    response = client.get("/api/frequencies?taraweeh_night=8")

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json["data"]) == 10
    assert response_json["total"] == 656
    assert response_json["data"][0] == {
        "lemma": "اللَّه",
        "root": "اله",
        "frequency": 109,
    }

    assert response_json["pagination"] == {
        "previous": None,
        "next": "/api/frequencies?offset=10&pagesize=10&taraweeh_night=8",
    }


def test_list_frequencies_with_taraweeh_night_and_pagination_params():
    response = client.get("/api/frequencies?taraweeh_night=8&offset=600&pagesize=100")

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json["data"]) == 56
    assert response_json["total"] == 656
    assert response_json["data"][0] == {
        "lemma": "كَفَى",
        "root": "كفي",
        "frequency": 1,
    }

    assert response_json["pagination"] == {
        "previous": "/api/frequencies?offset=500&pagesize=100&taraweeh_night=8",
        "next": None,
    }
