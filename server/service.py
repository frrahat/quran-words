from typing import Optional

from server.db_words_80_percent import db_words_80_percent, Level, Word as Words80Percent
from server.db_corpus import db_corpus, Corpus
from server.db_quran_arabic import db_quran_arabic, QuranArabic
from server.db_quran_english import db_quran_english, QuranEnglish
from server.db_words import db_words, Word


def list_word_80_percent_levels(offset: int, pagesize: int):
    base_query = db_words_80_percent.session.query(Level)
    total = base_query.count()

    levels = base_query.offset(offset).limit(pagesize).all()

    levels_data = [
            {
                'num': level.num,
                'title': level.title,
            } for level in levels
        ]

    return levels_data, total


def list_word_80_percent_words(offset: int, pagesize: int, level: Optional[int]):
    base_query = db_words_80_percent.session.query(Words80Percent)

    if level:
        base_query = base_query.filter(Words80Percent.level_num == level)

    total = base_query.count()

    words = base_query.order_by(Words80Percent.level_num, Words80Percent.serial_num).offset(
        offset).limit(pagesize).all()

    words_data = [
            {
                'level': word.level_num,
                'serial': word.serial_num,
                'arabic': word.arabic,
                'english': word.english,
            } for word in words
        ]
    return words_data, total


def list_sura_verses(sura_num: int, offset: int, pagesize: int):
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

    return verses, mapped_english_verse_text, total


def get_verse(sura_num: int, ayah_num: int):
    base_query = db_quran_arabic.session.query(
        QuranArabic).filter(QuranArabic.sura_num == sura_num)

    total_ayat = base_query.count()

    verse = base_query.filter(QuranArabic.ayah_num == ayah_num).first()
    verse_english = db_quran_english.session.query(
        QuranEnglish).filter(QuranEnglish.sura_num == sura_num, QuranEnglish.ayah_num == ayah_num).first()

    return verse, verse_english, total_ayat


def list_corpus(sura_num: int, ayah_num: int):
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
