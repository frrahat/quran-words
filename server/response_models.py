from typing import List, Optional

from pydantic import BaseModel


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
    arabic: str
    pos: str
    pos_full: Optional[str]
    pos_color: Optional[str]


class VerbFormsModel(BaseModel):
    root: str
    verb_type: str
    perfect: str
    imperative: str
    active_participle: str
    passive_participle: str
    verbal_noun: str


class CorpusWord(BaseModel):
    word_num: int
    segments: List[WordSegmentModel]
    root: str
    lemma: Optional[str]
    arabic: Optional[str]
    english: Optional[str]
    verb_type: Optional[str]
    verb_form: Optional[int]
    verb_forms: Optional[VerbFormsModel]


class CorpusResponseModel(BaseModel):
    sura: int
    ayah: int
    arabic: str
    english: str
    words: List[CorpusWord]


class WordRootOccurrenceVerseWord(BaseModel):
    word_num: int
    english: str


class WordRootOccurrenceVerse(BaseModel):
    arabic: str
    english: str
    words: List[WordRootOccurrenceVerseWord]


class WordRootOccurrence(BaseModel):
    sura: int
    ayah: int
    verse: WordRootOccurrenceVerse
    word_nums: List[int]


class WordRootOccurrencesResponseModel(BaseModel):
    root: str
    data: List[WordRootOccurrence]
    total: int
    pagination: PaginationResponseModel
