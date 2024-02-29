import itertools
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Dict, List, Optional, Tuple, Type, Union

from sqlalchemy import and_
from sqlalchemy import desc as sqlalchemy_desc
from sqlalchemy import func as sqlalchemy_func
from sqlalchemy import or_

from app.db.db_corpus import Corpus
from app.db.db_quran_arabic import QuranArabic
from app.db.db_quran_english import QuranEnglish
from app.db.db_words import Word
from app.taraweeh_ayat import get_start_end_ayah_by_night


class VERSE_LANG(Enum):
    ARABIC = "arabic"
    ENGLISH = "english"


@cache
def _get_verse(
    sura_num: int, ayah_num: int, type_: VERSE_LANG
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


@cache
def _get_words(sura_num: int, ayah_num: int) -> List[Word]:
    with Word.get_session() as session:
        return (
            session.query(Word)
            .filter(Word.sura_num == sura_num, Word.ayah_num == ayah_num)
            .order_by(Word.word_num)
            .all()
        )


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


def _get_occurrence_verses(verse_args: List[Tuple[int, int]]) -> List[Dict]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        verses_arabic = list(
            executor.map(
                _get_verse, *zip(*verse_args), itertools.repeat(VERSE_LANG.ARABIC)
            )
        )
        verses_english = list(
            executor.map(
                _get_verse, *zip(*verse_args), itertools.repeat(VERSE_LANG.ENGLISH)
            )
        )
        words_english = list(executor.map(_get_words, *zip(*verse_args)))

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


def _get_occrrences_in_verse(
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


@dataclass
class CorpusData:
    sura: int
    ayah: int
    arabic: str
    english: str
    words: List[Dict]


async def get_corpus(sura_num: int, ayah_num: int) -> Optional[CorpusData]:
    with ThreadPoolExecutor(max_workers=3) as executor:
        verse_arabic_future = executor.submit(
            _get_verse, sura_num, ayah_num, VERSE_LANG.ARABIC
        )
        verse_english_future = executor.submit(
            _get_verse, sura_num, ayah_num, VERSE_LANG.ENGLISH
        )
        words_future = executor.submit(_get_words, sura_num, ayah_num)

    verse_arabic = verse_arabic_future.result()
    verse_english = verse_english_future.result()
    words_english = words_future.result()

    if not verse_arabic:
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

    return CorpusData(
        sura=sura_num,
        ayah=ayah_num,
        arabic=str(verse_arabic.text),
        english=str(verse_english.text),
        words=words,
    )


@dataclass
class OccurrenceData:
    sura: int
    ayah: int
    verse: Dict
    word_nums: List[int]


async def list_occurrences(
    offset: int,
    pagesize: int,
    root: Optional[str],
    lemma: Optional[str],
    taraweeh_night: Optional[int],
) -> Tuple[List[OccurrenceData], int, int]:
    with Corpus.get_session() as session_corpus:
        base_query = session_corpus.query(Corpus.sura_num, Corpus.ayah_num)

        if root:
            base_query = base_query.filter(Corpus.root == root)

        if lemma:
            base_query = base_query.filter(Corpus.lemma == lemma)

        if not (root or lemma):
            raise ValueError("missing both root and lemma in query param")

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

    with ThreadPoolExecutor(max_workers=10) as executor:
        occurrence_word_nums = list(
            executor.map(
                _get_occrrences_in_verse,
                *zip(*occurrence_verse_args),
                itertools.repeat(root),
                itertools.repeat(lemma),
            )
        )
        occurrence_verses = list(
            executor.map(_get_occurrence_verses, [occurrence_verse_args])
        )[0]

    data = [
        OccurrenceData(
            sura=occurrence_verse_args[i][0],
            ayah=occurrence_verse_args[i][1],
            verse=occurrence_verses[i],
            word_nums=occurrence_word_nums[i],
        )
        for i in range(len(occurrence_verse_args))
    ]

    return data, total_verses, total_occurrences


@dataclass
class FrequencyData:
    root: Optional[str]
    lemma: str
    frequency: int


def list_frequencies(
    offset: int, pagesize: int, taraweeh_night: Optional[int]
) -> Tuple[List[FrequencyData], int]:
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

    data = [
        FrequencyData(
            root=row[0],
            lemma=row[1],
            frequency=row[2],
        )
        for row in frequencies
    ]
    return data, total
