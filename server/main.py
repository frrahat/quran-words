from typing import Dict, List, Optional
import urllib.parse

from fastapi import Depends, FastAPI, Path, Query, Request, Response, status

from server.response_models import (
    LevelListResponseModel,
    WordListResponseModel,
    VerseListResponseModel,
    VerseResponseModelForSingleAyah,
    CorpusResponseModel,
)
from server import service
from server.dependencies import pagination_parameters
from server.utils import get_pagination_response
from server.config import CONFIG

app = FastAPI()


@app.get('/')
def read_root():
    return 'hello world'


@app.get('/words-80-percent/levels', response_model=LevelListResponseModel)
def list_word_80_percent_levels(request: Request, pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    levels_data, total = service.list_word_80_percent_levels(offset, pagesize)

    return {
        'data': levels_data,
        'total': total,
        'pagination': get_pagination_response(request, total)
    }


@app.get('/words-80-percent/words', response_model=WordListResponseModel)
def list_word_80_percent_words(request: Request, level: Optional[int] = Query(None, gt=0), pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    words_data, total = service.list_word_80_percent_words(offset, pagesize, level)

    additional_query_string = f'level={level}' if level else ''

    return {
        'data': words_data,
        'total': total,
        'pagination': get_pagination_response(request, total, additional_query_string)
    }


@app.get('/verses/sura/{sura_num}', response_model=VerseListResponseModel)
def list_sura_verses(request: Request,
                     sura_num: int = Path(..., gt=0, le=114),
                     pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    verses, mapped_english_verse_text, total = service.list_sura_verses(
        sura_num, offset, pagesize)

    return {
        'data': [
            {
                'sura': verse.sura_num,
                'ayah': verse.ayah_num,
                'arabic': verse.text,
                'english': mapped_english_verse_text[verse.ayah_num],
                'links': {
                    'self': f'{CONFIG.BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num}',
                }
            } for verse in verses
        ],
        'total': total,
        'pagination': get_pagination_response(request, total)
    }


@app.get('/verses/sura/{sura_num}/ayah/{ayah_num}', response_model=VerseResponseModelForSingleAyah)
def get_verse(response: Response,
              sura_num: int = Path(..., gt=0, le=114),
              ayah_num: int = Path(..., gt=0, le=286)):

    verse, verse_english, total_ayat = service.get_verse(sura_num, ayah_num)

    if not verse:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    return {
        'sura': verse.sura_num,
        'ayah': verse.ayah_num,
        'arabic': verse.text,
        'english': verse_english.text,
        'links': {
            'self': f'{CONFIG.BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num}',
            'corpus': f'{CONFIG.BASE_URL}/corpus/sura/{sura_num}/ayah/{verse.ayah_num}',
            'prev': f'{CONFIG.BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num - 1}' if verse.ayah_num > 1 else None,
            'next': f'{CONFIG.BASE_URL}/verses/sura/{sura_num}/ayah/{verse.ayah_num + 1}' if verse.ayah_num < total_ayat else None,
        }
    }


@app.get('/corpus/sura/{sura_num}/ayah/{ayah_num}', response_model=List[CorpusResponseModel])
def list_corpus(sura_num: int = Path(..., gt=0, le=114),
                ayah_num: int = Path(..., gt=0, le=286)):

    words = service.list_corpus(sura_num, ayah_num)
    return words
