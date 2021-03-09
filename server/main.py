from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel

from .db import db, Level, Word, Verse


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


class VerseResponseModel(BaseModel):
    sura: int
    ayah: int
    arabic: str
    english: str


class VerseListResponseModel(BaseModel):
    data: List[VerseResponseModel]
    total: int
    pagination: PaginationResponseModel


def get_pagination_response(
                url: str,
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

    return {
        'previous': f'{url}?offset={prev_offset}&pagesize={prev_pagesize}{additional_query_string}' \
            if current_offset > 0 else None,
        'next': f'{url}?offset={next_offset}&pagesize={next_pagesize}{additional_query_string}' \
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


@app.get('/levels', response_model=LevelListResponseModel)
def list_level(pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db.session.query(Level)
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
        'pagination': get_pagination_response(f'{BASE_URL}/labels', total, offset, pagesize)
    }


@app.get('/words', response_model=WordListResponseModel)
def list_word(level: Optional[int] = Query(None, gt=0), pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db.session.query(Word)

    if level:
        base_query = base_query.filter(Word.level_num == level)

    total = base_query.count()

    words = base_query.order_by(Word.level_num, Word.serial_num).offset(offset).limit(pagesize).all()

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
            f'{BASE_URL}/words', total, offset, pagesize, additional_query_string)
    }


@app.get('/verses', response_model=VerseListResponseModel)
def list_verse(sura: Optional[int] = Query(None, gt=0, le=114),
               ayah: Optional[int] = Query(None, gt=0, le=286),
               pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db.session.query(Verse)

    if sura:
        base_query = base_query.filter(Verse.sura_num == sura)

    if ayah:
        base_query = base_query.filter(Verse.ayah_num == ayah)

    total = base_query.count()

    verses = base_query.order_by(Verse.sura_num, Verse.ayah_num).offset(offset).limit(pagesize).all()

    additional_query_string = '&'.join(f'{k}={v}' for k, v in {'sura': sura, 'ayah': ayah}.items() if v)
    return {
        'data': [
            {
                'sura': verse.sura_num,
                'ayah': verse.ayah_num,
                'arabic': verse.text,
                'english': '<Not available>',
            } for verse in verses
        ],
        'total': total,
        'pagination': get_pagination_response(
            f'{BASE_URL}/verses', total, offset, pagesize, additional_query_string)
    }
