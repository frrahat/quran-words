from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.config import CONFIG
from app.db_quran_arabic import db_quran_arabic, QuranArabic
from app.db_quran_english import db_quran_english, QuranEnglish
from app.taraweeh_ayat import get_start_end_ayah_by_day

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_read_app():
    response = client.get("/app")
    assert response.status_code == 200


def test_read_app_path():
    response = client.get("/app/something")
    assert response.status_code == 200


def test_list_word_80_percent_levels():
    response = client.get("/api/words-80-percent/levels")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["pagination"] == {
        "previous": None,
        "next": f"{CONFIG.BASE_URL}/api/words-80-percent/levels"
        f"?offset=10&pagesize=10",
    }


def test_list_word_80_percent_levels_with_pagesize_param():
    response = client.get("/api/words-80-percent/levels?offset=4&pagesize=6")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["data"]) == 6
    assert response_json["data"][0]["num"] == 5

    assert response_json["pagination"] == {
        "previous": f"{CONFIG.BASE_URL}/api/words-80-percent/levels"
        f"?offset=0&pagesize=4",
        "next": f"{CONFIG.BASE_URL}/api/words-80-percent/levels"
        f"?offset=10&pagesize=6",
    }


def test_list_word_80_percent_words():
    response = client.get("/api/words-80-percent/words")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["pagination"] == {
        "previous": None,
        "next": f"{CONFIG.BASE_URL}/api/words-80-percent/words"
        f"?offset=10&pagesize=10",
    }


def test_list_word_80_percent_words_with_pagesize_param():
    response = client.get("/api/words-80-percent/words?offset=7&pagesize=12")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["data"]) == 12
    assert response_json["data"][0]["serial"] == 8

    assert response_json["pagination"] == {
        "previous": f"{CONFIG.BASE_URL}/api/words-80-percent/words"
        f"?offset=0&pagesize=7",
        "next": f"{CONFIG.BASE_URL}/api/words-80-percent/words"
        f"?offset=19&pagesize=12",
    }


def test_list_verses_by_surah():
    response = client.get("/api/verses/sura/2")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["pagination"] == {
        "previous": None,
        "next": f"{CONFIG.BASE_URL}/api/verses/sura/2?offset=10&pagesize=10",
    }


def test_list_verses_by_surah_with_pagesize_param():
    response = client.get("/api/verses/sura/2?offset=14&pagesize=19")
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json["data"]) == 19
    assert response_json["data"][0]["ayah"] == 15

    assert response_json["pagination"] == {
        "previous": f"{CONFIG.BASE_URL}/api/verses/sura/2" f"?offset=0&pagesize=14",
        "next": f"{CONFIG.BASE_URL}/api/verses/sura/2" f"?offset=33&pagesize=19",
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
            "arabic": (
                db_quran_arabic.session.query(QuranArabic)
                .filter(QuranArabic.sura_num == 1, QuranArabic.ayah_num == 2)
                .first()
                .text
            ),
            "english": (
                db_quran_english.session.query(QuranEnglish)
                .filter(QuranEnglish.sura_num == 1, QuranEnglish.ayah_num == 2)
                .first()
                .text
            ),
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
        "next": f"{CONFIG.BASE_URL}/api/occurrences"
        f"?offset=10&pagesize=10&root={root}",
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
            "arabic": (
                db_quran_arabic.session.query(QuranArabic)
                .filter(QuranArabic.sura_num == 2, QuranArabic.ayah_num == 32)
                .first()
                .text
            ),
            "english": (
                db_quran_english.session.query(QuranEnglish)
                .filter(QuranEnglish.sura_num == 2, QuranEnglish.ayah_num == 32)
                .first()
                .text
            ),
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
        "previous": f"{CONFIG.BASE_URL}/api/occurrences"
        f"?offset=0&pagesize=7&root={root}",
        "next": f"{CONFIG.BASE_URL}/api/occurrences"
        f"?offset=15&pagesize=8&root={root}",
    }


@pytest.mark.parametrize("taraweeh_day", range(1, 28))
def test_list_occurrences_with_taraweeh_day_param(taraweeh_day):
    root = "علم"
    response = client.get(
        f"/api/occurrences?root={root}&taraweeh_day={taraweeh_day}&page_size=1000"
    )

    assert response.status_code == 200
    response_json = response.json()

    assert len(response_json["data"]) >= 2

    sura_ayah_list = [
        (occurrence["sura"], occurrence["ayah"]) for occurrence in response_json["data"]
    ]
    sorted_sura_ayah_list = sorted(sura_ayah_list)

    upper_limit_ayah, lower_limit_ayah = get_start_end_ayah_by_day(taraweeh_day)
    assert sorted_sura_ayah_list[0] >= (upper_limit_ayah.sura, upper_limit_ayah.ayah)
    assert sorted_sura_ayah_list[-1] <= (lower_limit_ayah.sura, lower_limit_ayah.ayah)