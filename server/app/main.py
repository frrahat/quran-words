from dataclasses import asdict
from typing import Optional

from fastapi import Depends, FastAPI, Path, Query, Request, Response, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app import service
from app.config import CONFIG
from app.db.db_quran_arabic import QuranArabic
from app.db.db_quran_english import QuranEnglish
from app.db.db_words_80_percent import Level
from app.db.db_words_80_percent import Word as Words80Percent
from app.dependencies import pagination_parameters
from app.response_models import (CorpusResponseModel, FrequenciesResponseModel,
                                 LevelListResponseModel,
                                 VerseListResponseModel,
                                 VerseResponseModelForSingleAyah,
                                 WordListResponseModel,
                                 WordRootOccurrencesResponseModel)
from app.utils import get_pagination_response

app = FastAPI()

app.mount("/public", StaticFiles(directory="client/build"), name="public")


@app.get("/")
def read_root():
    return RedirectResponse("/app")


@app.get("/app/{rest_of_path:path}")
def read_app():
    return FileResponse("client/build/index.html")


@app.get("/api/words-80-percent/levels", response_model=LevelListResponseModel)
def list_word_80_percent_levels(
    request: Request, pagination_params: dict = Depends(pagination_parameters)
):
    offset = pagination_params["offset"]
    pagesize = pagination_params["pagesize"]

    with Words80Percent.get_session() as session:
        base_query = session.query(Level)
        total = base_query.count()

        levels = base_query.offset(offset).limit(pagesize).all()

    return {
        "data": [
            {
                "num": level.num,
                "title": level.title,
            }
            for level in levels
        ],
        "total": total,
        "pagination": get_pagination_response(request, total),
    }


@app.get("/api/words-80-percent/words", response_model=WordListResponseModel)
def list_word_80_percent_words(
    request: Request,
    level: Optional[int] = Query(None, gt=0),
    pagination_params: dict = Depends(pagination_parameters),
):
    offset = pagination_params["offset"]
    pagesize = pagination_params["pagesize"]

    with Words80Percent.get_session() as session:
        base_query = session.query(Words80Percent)

        if level:
            base_query = base_query.filter(Words80Percent.level_num == level)

        total = base_query.count()

        words = (
            base_query.order_by(Words80Percent.level_num, Words80Percent.serial_num)
            .offset(offset)
            .limit(pagesize)
            .all()
        )

    additional_query_string = f"level={level}"

    return {
        "data": [
            {
                "level": word.level_num,
                "serial": word.serial_num,
                "arabic": word.arabic,
                "english": word.english,
            }
            for word in words
        ],
        "total": total,
        "pagination": get_pagination_response(request, total, additional_query_string),
    }


@app.get("/api/verses/sura/{sura_num}", response_model=VerseListResponseModel)
def list_sura_verses(
    request: Request,
    sura_num: int = Path(..., gt=0, le=114),
    pagination_params: dict = Depends(pagination_parameters),
):
    offset = pagination_params["offset"]
    pagesize = pagination_params["pagesize"]

    with QuranArabic.get_session() as session_quran_arabic:
        base_query = session_quran_arabic.query(QuranArabic).filter(
            QuranArabic.sura_num == sura_num
        )
        total = base_query.count()

        verses = (
            base_query.order_by(QuranArabic.ayah_num)
            .offset(offset)
            .limit(pagesize)
            .all()
        )

    with QuranEnglish.get_session() as session_quran_english:
        verses_english = (
            session_quran_english.query(QuranEnglish)
            .filter(QuranEnglish.sura_num == sura_num)
            .offset(offset)
            .limit(pagesize)
            .all()
        )

    mapped_english_verse_text = {verse.ayah_num: verse.text for verse in verses_english}

    return {
        "data": [
            {
                "sura": verse.sura_num,
                "ayah": verse.ayah_num,
                "arabic": verse.text,
                "english": mapped_english_verse_text[verse.ayah_num],
                "links": {
                    "self": f"{CONFIG.BASE_URL}"
                    f"/verses/sura/{sura_num}/ayah/{verse.ayah_num}",
                },
            }
            for verse in verses
        ],
        "total": total,
        "pagination": get_pagination_response(request, total),
    }


@app.get(
    "/api/verses/sura/{sura_num}/ayah/{ayah_num}",
    response_model=VerseResponseModelForSingleAyah,
)
def get_verse(
    response: Response,
    sura_num: int = Path(..., gt=0, le=114),
    ayah_num: int = Path(..., gt=0, le=286),
):
    with QuranArabic.get_session() as session_quran_arabic:
        base_query = session_quran_arabic.query(QuranArabic).filter(
            QuranArabic.sura_num == sura_num
        )

        total_ayat = base_query.count()

        verse = base_query.filter(QuranArabic.ayah_num == ayah_num).first()

    with QuranEnglish.get_session() as session_quran_english:
        verse_english = (
            session_quran_english.query(QuranEnglish)
            .filter(
                QuranEnglish.sura_num == sura_num, QuranEnglish.ayah_num == ayah_num
            )
            .first()
        )

    if not verse:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    sura_url = f"{CONFIG.BASE_URL}/verses/sura/{sura_num}"

    return {
        "sura": verse.sura_num,
        "ayah": verse.ayah_num,
        "arabic": verse.text,
        "english": verse_english.text,
        "links": {
            "self": f"{sura_url}/ayah/{verse.ayah_num}",
            "corpus": f"{CONFIG.BASE_URL}/corpus"
            f"/sura/{sura_num}/ayah/{verse.ayah_num}",
            "prev": (
                f"{sura_url}/ayah/{verse.ayah_num - 1}" if verse.ayah_num > 1 else None
            ),
            "next": (
                f"{sura_url}/ayah/{verse.ayah_num + 1}"
                if verse.ayah_num < total_ayat
                else None
            ),
        },
    }


@app.get(
    "/api/corpus/sura/{sura_num}/ayah/{ayah_num}", response_model=CorpusResponseModel
)
async def get_corpus(
    response: Response,
    sura_num: int = Path(..., gt=0, le=114),
    ayah_num: int = Path(..., gt=0, le=286),
):

    corpus = await service.get_corpus(sura_num, ayah_num)
    if not corpus:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    return {
        "sura": corpus.sura,
        "ayah": corpus.ayah,
        "arabic": corpus.arabic,
        "english": corpus.english,
        "words": corpus.words,
    }


@app.get("/api/occurrences", response_model=WordRootOccurrencesResponseModel)
async def list_occurrences(
    request: Request,
    root: Optional[str] = Query(None),
    lemma: Optional[str] = Query(None),
    taraweeh_night: Optional[int] = Query(None, ge=1, le=27),
    pagination_params: dict = Depends(pagination_parameters),
):
    offset = pagination_params["offset"]
    pagesize = pagination_params["pagesize"]

    data, total_verses, total_occurrences = await service.list_occurrences(
        offset, pagesize, root=root, lemma=lemma, taraweeh_night=taraweeh_night
    )

    return {
        "root": root,
        "lemma": lemma,
        "data": [asdict(item) for item in data],
        "total_occurrences": total_occurrences,
        "total": total_verses,
        "pagination": get_pagination_response(
            request,
            total_verses,
            additional_query_string=f"root={root}&lemma={lemma}",
        ),
    }


@app.get("/api/frequencies", response_model=FrequenciesResponseModel)
async def list_frequencies(
    request: Request,
    taraweeh_night: Optional[int] = Query(None, ge=1, le=27),
    pagination_params: dict = Depends(pagination_parameters),
):
    offset = pagination_params["offset"]
    pagesize = pagination_params["pagesize"]

    data, total = service.list_frequencies(
        offset, pagesize, taraweeh_night=taraweeh_night
    )
    return {
        "data": [asdict(item) for item in data],
        "total": total,
        "pagination": get_pagination_response(
            request,
            total,
            additional_query_string=f"taraweeh_night={taraweeh_night}",
        ),
    }
