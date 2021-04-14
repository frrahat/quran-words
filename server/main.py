from typing import Dict, List, Optional, Union
import urllib.parse

from fastapi import Depends, FastAPI, Path, Query, Request, Response, status
from pydantic import BaseModel

from server.db_words_80_percent import db_words_80_percent, Level, Word as Words80Percent
from server.db_corpus import db_corpus, Corpus
from server.db_quran_arabic import db_quran_arabic, QuranArabic
from server.db_quran_english import db_quran_english, QuranEnglish
from server.db_words import db_words, Word


app = FastAPI()


BASE_URL = 'http://localhost:8000'


class PaginationResponseModel(BaseModel):
    previous: Optional[str]
    next: Optional[str]


class LevelResponseModel(BaseModel):
    num: int
    title: str


class LevelListResponseModel(BaseModel):
    data: List[LevelResponseModel]
    total: int
    pagination: PaginationResponseModel


class WordResponseModel(BaseModel):
    level: int
    serial: int
    arabic: str
    english: str


class WordListResponseModel(BaseModel):
    data: List[WordResponseModel]
    total: int
    pagination: PaginationResponseModel


class VerseLinks(BaseModel):
    self: str


class VerseLinksResponseModelForSingleAyah(VerseLinks):
    corpus: str
    prev: Optional[str]
    next: Optional[str]


class VerseResponseModel(BaseModel):
    sura: int
    ayah: int
    arabic: str
    english: str
    links: VerseLinks


class VerseResponseModelForSingleAyah(VerseResponseModel):
    links: VerseLinksResponseModelForSingleAyah


class VerseListResponseModel(BaseModel):
    data: List[VerseResponseModel]
    total: int
    pagination: PaginationResponseModel


class WordSegmentModel(BaseModel):
    segment: str
    pos: str


class VerbFormsModel(BaseModel):
    root: str
    verb_type: str
    perfect: str
    imperative: str
    active_participle: str
    passive_participle: str
    verbal_noun: str


class CorpusResponseModel(BaseModel):
    sura: int
    ayah: int
    word_num: int
    segments: List[WordSegmentModel]
    root: str
    lemma: Optional[str]
    verb_type: Optional[str]
    verb_form: Optional[int]
    verb_forms: Optional[VerbFormsModel]


def get_pagination_response(
        request: Request,
        count: int,
        current_offset: int,
        current_pagesize: int,
        additional_query_string: Optional[str] = None,
        limit: int = 10) -> Dict[str, Optional[str]]:

    prev_offset = max(0, current_offset - limit)
    prev_pagesize = min(limit, count, current_offset)

    next_offset = current_offset + current_pagesize
    next_pagesize = min(next_offset + limit, count - next_offset + 1)

    additional_query_string = f'&{additional_query_string}' if additional_query_string else ''

    url = urllib.parse.urljoin(str(request.base_url), request.url.path)

    return {
        'previous': f'{url}?offset={prev_offset}&pagesize={prev_pagesize}{additional_query_string}'
        if current_offset > 0 else None,
        'next': f'{url}?offset={next_offset}&pagesize={next_pagesize}{additional_query_string}'
        if next_offset < count else None,
    }


@app.get('/')
def read_root():
    return 'hello world'


def pagination_parameters(offset: Optional[int] = Query(0, ge=0),
                          pagesize: Optional[int] = Query(10, gt=0)):
    return {
        'offset': offset,
        'pagesize': pagesize,
    }


@app.get('/words-80-percent/levels', response_model=LevelListResponseModel)
def list_word_80_percent_levels(request: Request, pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db_words_80_percent.session.query(Level)
    total = base_query.count()

    levels = base_query.offset(offset).limit(pagesize).all()

    return {
        'data': [
            {
                'num': level.num,
                'title': level.title,
            } for level in levels
        ],
        'total': total,
        'pagination': get_pagination_response(request, total, offset, pagesize)
    }


@app.get('/words-80-percent/words', response_model=WordListResponseModel)
def list_word_80_percent_words(request: Request, level: Optional[int] = Query(None, gt=0), pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db_words_80_percent.session.query(Words80Percent)

    if level:
        base_query = base_query.filter(Words80Percent.level_num == level)

    total = base_query.count()

    words = base_query.order_by(Words80Percent.level_num, Words80Percent.serial_num).offset(
        offset).limit(pagesize).all()

    additional_query_string = f'level={level}' if level else ''

    return {
        'data': [
            {
                'level': word.level_num,
                'serial': word.serial_num,
                'arabic': word.arabic,
                'english': word.english,
            } for word in words
        ],
        'total': total,
        'pagination': get_pagination_response(
            request, total, offset, pagesize, additional_query_string)
    }


@app.get('/verses/sura/{sura_num}', response_model=VerseListResponseModel)
def list_sura_verses(request: Request,
                     sura_num: int = Path(..., gt=0, le=114),
                     pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db_quran_arabic.session.query(
        QuranArabic).filter(QuranArabic.sura_num == sura_num)
    total = base_query.count()

    verses = base_query.order_by(QuranArabic.ayah_num).offset(
        offset).limit(pagesize).all()

    return {
        'data': [
            {
                'sura': verse.sura_num,
                'ayah': verse.ayah_num,
                'arabic': verse.text,
                'english': '<Not available>',
                'links': {
                    'self': f'{BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num}',
                }
            } for verse in verses
        ],
        'total': total,
        'pagination': get_pagination_response(
            request, total, offset, pagesize)
    }


@app.get('/verses/sura/{sura_num}/ayah/{ayah_num}', response_model=VerseResponseModelForSingleAyah)
def get_verse(response: Response,
              sura_num: int = Path(..., gt=0, le=114),
              ayah_num: int = Path(..., gt=0, le=286)):

    base_query = db_quran_arabic.session.query(
        QuranArabic).filter(QuranArabic.sura_num == sura_num)

    total_ayat = base_query.count()

    verse = base_query.filter(QuranArabic.ayah_num == ayah_num).first()

    if not verse:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    return {
        'sura': verse.sura_num,
        'ayah': verse.ayah_num,
        'arabic': verse.text,
        'english': '<Not available>',
        'links': {
            'self': f'{BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num}',
            'corpus': f'{BASE_URL}/corpus/sura/{sura_num}/ayah/{verse.ayah_num}',
            'prev': f'{BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num - 1}' if verse.ayah_num > 1 else None,
            'next': f'{BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num + 1}' if verse.ayah_num < total_ayat else None,
        }
    }


@app.get('/corpus/sura/{sura_num}/ayah/{ayah_num}', response_model=List[CorpusResponseModel])
def list_corpus(sura_num: int = Path(..., gt=0, le=114),
                ayah_num: int = Path(..., gt=0, le=286)):

    base_query = db_corpus.session.query(Corpus).filter(
        Corpus.sura_num == sura_num, Corpus.ayah_num == ayah_num)
    ordered_corpus_list = base_query.order_by(Corpus.word_num).all()

    words = []

    for corpus in ordered_corpus_list:
        verb_forms = corpus.verb_forms
        word = {
            'sura': corpus.sura_num,
            'ayah': corpus.ayah_num,
            'word_num': corpus.word_num,
            'segments': corpus.get_segments(),
            'root': corpus.root,
            'lemma': corpus.lemma,
            'verb_type': corpus.verb_type,
            'verb_form': corpus.verb_form,
            'verb_forms': {
                'root': verb_forms.root,
                'verb_type': verb_forms.verb_type,
                'perfect': verb_forms.perfect,
                'imperative': verb_forms.imperative,
                'active_participle': verb_forms.active_participle,
                'passive_participle': verb_forms.passive_participle,
                'verbal_noun': verb_forms.verbal_noun,
            } if verb_forms else None,
        }

        words.append(word)

    return words
