import asyncio
from enum import Enum
from typing import Dict, List, Optional, Tuple, Type, Union

from fastapi import (Depends, FastAPI, HTTPException, Path, Query, Request,
                     Response, status)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import and_
from sqlalchemy import desc as sqlalchemy_desc
from sqlalchemy import func as sqlalchemy_func
from sqlalchemy import or_
from starlette.responses import RedirectResponse

from app.config import CONFIG
from app.db.db_corpus import Corpus
from app.db.db_quran_arabic import QuranArabic
from app.db.db_quran_english import QuranEnglish
from app.db.db_words import Word
from app.db.db_words_80_percent import Level
from app.db.db_words_80_percent import Word as Words80Percent
from app.dependencies import pagination_parameters
from app.response_models import (CorpusResponseModel, FrequenciesResponseModel,
                                 LevelListResponseModel,
                                 VerseListResponseModel,
                                 VerseResponseModelForSingleAyah,
                                 WordListResponseModel,
                                 WordRootOccurrencesResponseModel)
from app.taraweeh_ayat import get_start_end_ayah_by_night
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


class VERSE_LANG(Enum):
    ARABIC = "arabic"
    ENGLISH = "english"


async def _get_verse(
    sura_num: int, ayah_num: int, type_: VERSE_LANG = VERSE_LANG.ARABIC
) -> Union[QuranArabic, QuranEnglish]:
    with (
        QuranArabic.get_session() as session_quran_arabic,
        QuranEnglish.get_session() as session_quran_english,
    ):
        db_session = (
            session_quran_arabic
            if type_ == VERSE_LANG.ARABIC
            else session_quran_english
        )
        model_cls: Union[Type[QuranArabic], Type[QuranEnglish]] = (
            QuranArabic if type_ == VERSE_LANG.ARABIC else QuranEnglish
        )
        return (
            db_session.query(model_cls)
            .filter(model_cls.sura_num == sura_num, model_cls.ayah_num == ayah_num)
            .first()
        )


async def _get_words(sura_num: int, ayah_num: int) -> List[Word]:
    with Word.get_session() as session:
        return (
            session.query(Word)
            .filter(Word.sura_num == sura_num, Word.ayah_num == ayah_num)
            .order_by(Word.word_num)
            .all()
        )


@app.get(
    "/api/corpus/sura/{sura_num}/ayah/{ayah_num}", response_model=CorpusResponseModel
)
async def get_corpus(
    response: Response,
    sura_num: int = Path(..., gt=0, le=114),
    ayah_num: int = Path(..., gt=0, le=286),
):
    verse_arabic, verse_english, words_english = await asyncio.gather(
        _get_verse(sura_num, ayah_num, type_=VERSE_LANG.ARABIC),
        _get_verse(sura_num, ayah_num, type_=VERSE_LANG.ENGLISH),
        _get_words(sura_num, ayah_num),
    )

    if not verse_arabic:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    words_arabic = verse_arabic.text.split(" ")
    mapped_arabic_words = {
        word_num: word for word_num, word in enumerate(words_arabic, 1)
    }

    mapped_english_words = {word.word_num: word.english for word in words_english}

    with Corpus.get_session() as session_corpus:
        base_query = session_corpus.query(Corpus).filter(
            Corpus.sura_num == sura_num, Corpus.ayah_num == ayah_num
        )
        ordered_corpus_list = base_query.order_by(Corpus.word_num).all()

    words = []

    for corpus in ordered_corpus_list:
        verb_forms = corpus.verb_forms
        word = {
            "word_num": corpus.word_num,
            "segments": corpus.get_segments(),
            "root": corpus.root,
            "lemma": corpus.lemma,
            "arabic": mapped_arabic_words.get(corpus.word_num),
            "english": mapped_english_words.get(corpus.word_num),
            "verb_type": corpus.verb_type,
            "verb_form": corpus.verb_form,
            "verb_forms": (
                {
                    "root": verb_forms.root,
                    "verb_type": verb_forms.verb_type,
                    "perfect": verb_forms.perfect,
                    "imperative": verb_forms.imperative,
                    "active_participle": verb_forms.active_participle,
                    "passive_participle": verb_forms.passive_participle,
                    "verbal_noun": verb_forms.verbal_noun,
                }
                if verb_forms
                else None
            ),
        }

        words.append(word)

    return {
        "sura": sura_num,
        "ayah": ayah_num,
        "arabic": verse_arabic.text,
        "english": verse_english.text,
        "words": words,
    }


async def _get_occurrence_verses(verse_args: List[Tuple[int, int]]) -> List[Dict]:
    verses_arabic_future = asyncio.gather(
        *(_get_verse(*arg, type_=VERSE_LANG.ARABIC) for arg in verse_args)
    )

    verses_english_future = asyncio.gather(
        *(_get_verse(*arg, type_=VERSE_LANG.ENGLISH) for arg in verse_args)
    )

    words_english_future = asyncio.gather(*(_get_words(*arg) for arg in verse_args))

    verses_arabic, verses_english, words_english = await asyncio.gather(
        verses_arabic_future,
        verses_english_future,
        words_english_future,
    )

    occurrence_verses = [
        {
            "arabic": verses_arabic[i].text,
            "english": verses_english[i].text,
            "words": [
                {
                    "word_num": word.word_num,
                    "english": word.english,
                }
                for word in words_english[i]
            ],
        }
        for i in range(len(verse_args))
    ]

    return occurrence_verses


async def _get_occrrences_in_verse(
    sura_num: int,
    ayah_num: int,
    root: Optional[str],
    lemma: Optional[str],
) -> List[int]:
    if not (root or lemma):
        raise ValueError("Both root and lemma are missing")

    with Corpus.get_session() as session_corpus:
        base_query = session_corpus.query(Corpus.word_num).filter(
            Corpus.sura_num == sura_num,
            Corpus.ayah_num == ayah_num,
        )

        if root:
            base_query = base_query.filter(Corpus.root == root)

        if lemma:
            base_query = base_query.filter(Corpus.lemma == lemma)

        word_nums_result = base_query.order_by(Corpus.word_num).all()

    return [row[0] for row in word_nums_result]


def _get_filter_arg_for_taraweeh_night(taraweeh_night):
    start_ayah_info, end_ayah_info = get_start_end_ayah_by_night(taraweeh_night)
    conditions = [
        and_(
            Corpus.sura_num == start_ayah_info.sura,
            Corpus.ayah_num >= start_ayah_info.ayah,
        ),
        and_(
            Corpus.sura_num > start_ayah_info.sura,
            Corpus.sura_num < end_ayah_info.sura,
        ),
        and_(
            Corpus.sura_num == end_ayah_info.sura, Corpus.ayah_num <= end_ayah_info.ayah
        ),
    ]

    return or_(*conditions)


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

    with Corpus.get_session() as session_corpus:
        base_query = session_corpus.query(Corpus.sura_num, Corpus.ayah_num)

        if root:
            base_query = base_query.filter(Corpus.root == root)

        if lemma:
            base_query = base_query.filter(Corpus.lemma == lemma)

        if not (root or lemma):
            raise HTTPException(
                status_code=422, detail="missing both root and lemma in query param"
            )

        if taraweeh_night:
            filter_arg = _get_filter_arg_for_taraweeh_night(taraweeh_night)
            base_query = base_query.filter(filter_arg)

        occurrences_verse_query = base_query.distinct()

        occurrence_verse_args: List[Tuple[int, int]] = (
            occurrences_verse_query.order_by(Corpus.sura_num, Corpus.ayah_num)
            .offset(offset)
            .limit(pagesize)
            .all()
        )

        total_occurrences = base_query.count()
        total_verses = occurrences_verse_query.count()

    word_nums_future = asyncio.gather(
        *(_get_occrrences_in_verse(*arg, root, lemma) for arg in occurrence_verse_args)
    )

    occurrence_verses, occurrence_word_nums = await asyncio.gather(
        _get_occurrence_verses(occurrence_verse_args),
        word_nums_future,
    )

    data = [
        {
            "sura": occurrence_verse_args[i][0],
            "ayah": occurrence_verse_args[i][1],
            "verse": occurrence_verses[i],
            "word_nums": occurrence_word_nums[i],
        }
        for i in range(len(occurrence_verse_args))
    ]

    return {
        "root": root,
        "lemma": lemma,
        "data": data,
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

    with Corpus.get_session() as session_corpus:
        base_query = (
            session_corpus.query(
                Corpus.root, Corpus.lemma, sqlalchemy_func.count(Corpus.lemma)
            )
            .filter(Corpus.lemma.isnot(None))
            .group_by(Corpus.root, Corpus.lemma)
            .order_by(sqlalchemy_desc(sqlalchemy_func.count(Corpus.lemma)))
        )

        if taraweeh_night:
            filter_arg = _get_filter_arg_for_taraweeh_night(taraweeh_night)
            base_query = base_query.filter(filter_arg)

        frequencies = base_query.offset(offset).limit(pagesize).all()
        total = base_query.count()

    return {
        "data": [
            {
                "root": row[0],
                "lemma": row[1],
                "frequency": row[2],
            }
            for row in frequencies
        ],
        "total": total,
        "pagination": get_pagination_response(
            request,
            total,
            additional_query_string=f"taraweeh_night={taraweeh_night}",
        ),
    }
