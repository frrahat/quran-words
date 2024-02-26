from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.schema import ForeignKeyConstraint

from app.db.common import SessionMakerMixin


class Base(SessionMakerMixin, DeclarativeBase):
    __db_filename__ = "corpus.db"


POS_FULL_FORMS_AND_COLORS = {
    "N": {
        "full": "Noun",
        "color": "#fff",
    },
    "PN": {
        "full": "Proper Noun",
        "color": "#fff",
    },
    "ADJ": {
        "full": "Adjective",
        "color": "#fff",
    },
    "IMPN": {
        "full": "Imperative verbal noun",
        "color": "#fff",
    },
    "PRON": {
        "full": "Personal pronoun",
        "color": "#fff",
    },
    "DEM": {
        "full": "Demonstrative pronoun",
        "color": "#fff",
    },
    "REL": {
        "full": "Relative pronoun",
        "color": "#fff",
    },
    "T": {
        "full": "Time adverb",
        "color": "#fff",
    },
    "LOC": {
        "full": "Location adverb",
        "color": "#fff",
    },
    "V": {
        "full": "Verb",
        "color": "#fff",
    },
    "P": {
        "full": "Preposition",
        "color": "#fff",
    },
    "EMPH": {
        "full": "Emphatic lām prefix",
        "color": "#fff",
    },
    "IMPV": {
        "full": "Imperative lām prefix",
        "color": "#fff",
    },
    "PRP": {
        "full": "Purpose lām prefix",
        "color": "#fff",
    },
    "CONJ": {
        "full": "Coordinating conjunction",
        "color": "#fff",
    },
    "SUB": {
        "full": "Subordinating conjunction",
        "color": "#fff",
    },
    "ACC": {
        "full": "Accusative particle",
        "color": "#fff",
    },
    "AMD": {
        "full": "Amendment particle",
        "color": "#fff",
    },
    "ANS": {
        "full": "Answer particle",
        "color": "#fff",
    },
    "AVR": {
        "full": "Aversion particle",
        "color": "#fff",
    },
    "CAUS": {
        "full": "Particle of cause",
        "color": "#fff",
    },
    "CERT": {
        "full": "Particle of certainty",
        "color": "#fff",
    },
    "CIRC": {
        "full": "Circumstantial particle",
        "color": "#fff",
    },
    "COM": {
        "full": "Comitative particle",
        "color": "#fff",
    },
    "COND": {
        "full": "Conditional particle",
        "color": "#fff",
    },
    "EQ": {
        "full": "Equalization particle",
        "color": "#fff",
    },
    "EXH": {
        "full": "Exhortation particle",
        "color": "#fff",
    },
    "EXL": {
        "full": "Explanation particle",
        "color": "#fff",
    },
    "EXP": {
        "full": "Exceptive particle",
        "color": "#fff",
    },
    "FUT": {
        "full": "Future particle",
        "color": "#fff",
    },
    "INC": {
        "full": "Inceptive particle",
        "color": "#fff",
    },
    "INT": {
        "full": "Particle of interpretation",
        "color": "#fff",
    },
    "INTG": {
        "full": "Interogative particle",
        "color": "#fff",
    },
    "NEG": {
        "full": "Negative particle",
        "color": "#fff",
    },
    "PREV": {
        "full": "Preventive particle",
        "color": "#fff",
    },
    "PRO": {
        "full": "Prohibition particle",
        "color": "#fff",
    },
    "REM": {
        "full": "Resumption particle",
        "color": "#fff",
    },
    "RES": {
        "full": "Restriction particle",
        "color": "#fff",
    },
    "RET": {
        "full": "Retraction particle",
        "color": "#fff",
    },
    "RSLT": {
        "full": "Result particle",
        "color": "#fff",
    },
    "SUP": {
        "full": "Supplemental particle",
        "color": "#fff",
    },
    "SUR": {
        "full": "Surprise particle",
        "color": "#fff",
    },
    "VOC": {
        "full": "Vocative particle",
        "color": "#fff",
    },
    "INL": {
        "full": "Quranic initials",
        "color": "#fff",
    },
    "ATT": {
        "full": "Attention",
        "color": "#fff",
    },
    "DET": {
        "full": "Determiner",
        "color": "#fff",
    },
    "DIST": {
        "full": "Distance",
        "color": "#fff",
    },
    "ADDR": {
        "full": "Address",
        "color": "#fff",
    },
    "NV": {
        "full": "Nounal Verb",
        "color": "#fff",
    },
}


class VerbForms(Base):
    __tablename__ = "verbs_with_six_forms"
    root = Column("root", Unicode, primary_key=True)
    verb_type = Column("verb_type", String(length=3), primary_key=True)
    perfect = Column("perfect", Unicode)
    imperfect = Column("imperfect", Unicode)
    imperative = Column("imperative", Unicode)
    active_participle = Column("active_participle", Unicode)
    passive_participle = Column("passive_participle", Unicode)
    verbal_noun = Column("verbal_noun", Unicode)

    def to_dict(self):
        return {
            "root": self.root,
            "verb_type": self.verb_type,
            "perfect": self.perfect,
            "imperative": self.imperative,
            "active_participle": self.active_participle,
            "passive_participle": self.passive_participle,
            "verbal_noun": self.verbal_noun,
        }


class Corpus(Base):
    __tablename__ = "corpus"
    sura_num = Column("surah", Integer, primary_key=True)
    ayah_num = Column("ayah", Integer, primary_key=True)
    word_num = Column("word", Integer, primary_key=True)
    count = Column("count", Integer)
    ar1 = Column("ar1", Unicode)
    ar2 = Column("ar2", Unicode)
    ar3 = Column("ar3", Unicode)
    ar4 = Column("ar4", Unicode)
    ar5 = Column("ar5", Unicode)
    pos1 = Column("pos1", Unicode)
    pos2 = Column("pos2", Unicode)
    pos3 = Column("pos3", Unicode)
    pos4 = Column("pos4", Unicode)
    pos5 = Column("pos5", Unicode)
    root = Column("root_ar", Unicode)
    lemma = Column("lemma", Unicode)
    verb_type = Column("verb_type", String(length=3))
    verb_form = Column("verf_form", Integer)
    verb_forms = relationship("VerbForms", uselist=False, lazy="joined")

    ForeignKeyConstraint([root, verb_type], [VerbForms.root, VerbForms.verb_type])

    def get_segments(self):
        segments = []

        for position in range(1, self.count + 1):
            arabic = getattr(self, f"ar{position}")
            pos = getattr(self, f"pos{position}")

            pos_full_form_and_color = POS_FULL_FORMS_AND_COLORS.get(
                pos, {"full": None, "color": None}
            )

            segments.append(
                {
                    "arabic": arabic,
                    "pos": pos,
                    "pos_full": pos_full_form_and_color["full"],
                    "pos_color": pos_full_form_and_color["color"],
                }
            )

        return segments


if __name__ == "__main__":
    with Corpus.get_session() as db_corpus:
        print(db_corpus.query(Corpus).count())
        print(db_corpus.query(VerbForms).count())

        base_query = (
            db_corpus.query(Corpus)
            .filter(Corpus.sura_num == 1, Corpus.ayah_num == 5, Corpus.word_num == 2)
            .first()
        )

        print(base_query.get_segments())
        print(base_query.verb_forms.to_dict())
