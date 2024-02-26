from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import DeclarativeBase

from app.db.common import SessionMakerMixin


class Base(SessionMakerMixin, DeclarativeBase):
    __db_filename__ = "quran_english.db"


class QuranEnglish(Base):
    __tablename__ = "verses"
    sura_num = Column("sura", Integer, primary_key=True)
    ayah_num = Column("ayah", Integer, primary_key=True)
    text = Column("text", Unicode)


if __name__ == "__main__":
    with QuranEnglish.get_session() as session:
        print(session.query(QuranEnglish).count())
