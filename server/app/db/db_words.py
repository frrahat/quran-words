from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import DeclarativeBase

from app.db.common import SessionMakerMixin


class Base(SessionMakerMixin, DeclarativeBase):
    __db_filename__ = "words.db"


class Word(Base):
    __tablename__ = "allwords"
    sura_num = Column("sura", Integer, primary_key=True)
    ayah_num = Column("ayah", Integer, primary_key=True)
    word_num = Column("word", Integer, primary_key=True)
    english = Column("en", Unicode)


if __name__ == "__main__":
    with Word.get_session() as session:
        print(session.query(Word).count())
