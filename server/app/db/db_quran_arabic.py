from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import DeclarativeBase

from app.db.common import SessionMakerMixin


class Base(SessionMakerMixin, DeclarativeBase):
    __db_filename__ = "quran_arabic.db"


class QuranArabic(Base):
    __tablename__ = "verses"
    sura_num = Column("sura", Integer, primary_key=True)
    ayah_num = Column("ayah", Integer, primary_key=True)
    text = Column("text", Unicode)


if __name__ == "__main__":
    with QuranArabic.get_session() as db_quran_arabic:
        print(db_quran_arabic.query(QuranArabic).count())
