from typing import Optional

from fastapi import Depends, FastAPI, Path, Query, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse

from server.db_words_80_percent import (
    db_words_80_percent, Level, Word as Words80Percent)
from server.db_corpus import db_corpus, Corpus
from server.db_quran_arabic import db_quran_arabic, QuranArabic
from server.db_quran_english import db_quran_english, QuranEnglish
from server.db_words import db_words, Word
from server.response_models import (
    LevelListResponseModel,
    WordListResponseModel,
    VerseListResponseModel,
    VerseResponseModelForSingleAyah,
    CorpusResponseModel,
    WordRootOccurrencesResponseModel,
)
from server.dependencies import pagination_parameters
from server.utils import get_pagination_response
from server.config import CONFIG

app = FastAPI()

app.mount('/public', StaticFiles(directory='client/build'), name='public')


@app.get('/')
def read_root():
    return RedirectResponse('/app')


@app.get('/app/{rest_of_path:path}')
def read_app():
    return FileResponse('client/build/index.html')


@app.get('/api/words-80-percent/levels', response_model=LevelListResponseModel)
def list_word_80_percent_levels(
        request: Request,
        pagination_parameters: dict = Depends(pagination_parameters)):
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
        'pagination': get_pagination_response(request, total)
    }


@app.get('/api/words-80-percent/words', response_model=WordListResponseModel)
def list_word_80_percent_words(
        request: Request,
        level: Optional[int] = Query(None, gt=0),
        pagination_parameters: dict = Depends(pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db_words_80_percent.session.query(Words80Percent)

    if level:
        base_query = base_query.filter(Words80Percent.level_num == level)

    total = base_query.count()

    words = base_query\
        .order_by(Words80Percent.level_num, Words80Percent.serial_num)\
        .offset(offset)\
        .limit(pagesize).all()

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
            request, total, additional_query_string)
    }


@app.get('/api/verses/sura/{sura_num}', response_model=VerseListResponseModel)
def list_sura_verses(request: Request,
                     sura_num: int = Path(..., gt=0, le=114),
                     pagination_parameters: dict = Depends(
                         pagination_parameters)):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db_quran_arabic.session.query(
        QuranArabic).filter(QuranArabic.sura_num == sura_num)
    total = base_query.count()

    verses = base_query.order_by(QuranArabic.ayah_num).offset(
        offset).limit(pagesize).all()

    verses_english = db_quran_english.session.query(
        QuranEnglish).filter(QuranEnglish.sura_num == sura_num).offset(
        offset).limit(pagesize).all()

    mapped_english_verse_text = {
        verse.ayah_num: verse.text for verse in verses_english
    }

    return {
        'data': [
            {
                'sura': verse.sura_num,
                'ayah': verse.ayah_num,
                'arabic': verse.text,
                'english': mapped_english_verse_text[verse.ayah_num],
                'links': {
                    'self': f'{CONFIG.BASE_URL}'
                    f'/verses/sura/{sura_num}/ayah/{verse.ayah_num}',
                }
            } for verse in verses
        ],
        'total': total,
        'pagination': get_pagination_response(request, total)
    }


@app.get('/api/verses/sura/{sura_num}/ayah/{ayah_num}',
         response_model=VerseResponseModelForSingleAyah)
def get_verse(response: Response,
              sura_num: int = Path(..., gt=0, le=114),
              ayah_num: int = Path(..., gt=0, le=286)):

    base_query = db_quran_arabic.session.query(
        QuranArabic).filter(QuranArabic.sura_num == sura_num)

    total_ayat = base_query.count()

    verse = base_query.filter(QuranArabic.ayah_num == ayah_num).first()
    verse_english = db_quran_english.session.query(
        QuranEnglish).filter(
            QuranEnglish.sura_num == sura_num,
            QuranEnglish.ayah_num == ayah_num).first()

    if not verse:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    sura_url = f'{CONFIG.BASE_URL}/verses/sura/{sura_num}'

    return {
        'sura': verse.sura_num,
        'ayah': verse.ayah_num,
        'arabic': verse.text,
        'english': verse_english.text,
        'links': {
            'self': f'{sura_url}/ayah/{verse.ayah_num}',
            'corpus': f'{CONFIG.BASE_URL}/corpus'
            f'/sura/{sura_num}/ayah/{verse.ayah_num}',
            'prev': f'{sura_url}/ayah/{verse.ayah_num - 1}'
            if verse.ayah_num > 1 else None,
            'next': f'{sura_url}/ayah/{verse.ayah_num + 1}'
            if verse.ayah_num < total_ayat else None,
        }
    }


@app.get('/api/corpus/sura/{sura_num}/ayah/{ayah_num}',
         response_model=CorpusResponseModel)
def get_corpus(response: Response,
               sura_num: int = Path(..., gt=0, le=114),
               ayah_num: int = Path(..., gt=0, le=286)):

    verse_arabic = db_quran_arabic.session.query(QuranArabic)\
        .filter(
            QuranArabic.sura_num == sura_num,
            QuranArabic.ayah_num == ayah_num).first()

    if not verse_arabic:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    verse_english = db_quran_english.session.query(QuranEnglish)\
        .filter(
            QuranEnglish.sura_num == sura_num,
            QuranEnglish.ayah_num == ayah_num).first()

    words_arabic = verse_arabic.text.split(' ')
    mapped_arabic_words = {word_num: word for word_num,
                           word in enumerate(words_arabic, 1)}

    words_english = db_words.session.query(Word).filter(
        Word.sura_num == sura_num, Word.ayah_num == ayah_num).all()
    mapped_english_words = {
        word.word_num: word.english for word in words_english}

    base_query = db_corpus.session.query(Corpus).filter(
        Corpus.sura_num == sura_num, Corpus.ayah_num == ayah_num)
    ordered_corpus_list = base_query.order_by(Corpus.word_num).all()

    words = []

    for corpus in ordered_corpus_list:
        verb_forms = corpus.verb_forms
        word = {
            'word_num': corpus.word_num,
            'segments': corpus.get_segments(),
            'root': corpus.root,
            'lemma': corpus.lemma,
            'arabic': mapped_arabic_words.get(corpus.word_num),
            'english': mapped_english_words.get(corpus.word_num),
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

    return {
        'sura': sura_num,
        'ayah': ayah_num,
        'arabic': verse_arabic.text,
        'english': verse_english.text,
        'words': words,
    }


@app.get('/api/occurrences',
         response_model=WordRootOccurrencesResponseModel)
def list_occurrences(request: Request,
                     root: str,
                     pagination_parameters: dict = Depends(
                         pagination_parameters
                     )):
    offset = pagination_parameters['offset']
    pagesize = pagination_parameters['pagesize']

    base_query = db_corpus.session.query(Corpus).filter(Corpus.root == root)

    occurrences = (base_query
                   .order_by(Corpus.sura_num, Corpus.ayah_num, Corpus.word_num)
                   .offset(offset)
                   .limit(pagesize)
                   .all())

    total = base_query.count()

    data = [
        {
            'sura': occurrence.sura_num,
            'ayah': occurrence.ayah_num,
            'word_num': occurrence.word_num,
        } for occurrence in occurrences
    ]

    return {
        'root': root,
        'data': data,
        'total': total,
        'pagination': get_pagination_response(
            request, total, additional_query_string=f'root={root}')
    }
