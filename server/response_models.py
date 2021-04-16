from typing import Dict, List, Optional, Union

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
