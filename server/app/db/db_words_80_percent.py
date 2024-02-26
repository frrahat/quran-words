from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.schema import ForeignKey, ForeignKeyConstraint

from app.db.common import SessionMakerMixin


class Base(SessionMakerMixin, DeclarativeBase):
    __db_filename__ = "words80percent.db"


class Level(Base):
    __tablename__ = "levels"
    num = Column("level_num", Integer, primary_key=True)
    title = Column("level_title", Unicode)


class Verse(Base):
    __tablename__ = "verses"
    sura_num = Column("sura_num", Integer, primary_key=True)
    ayah_num = Column("ayah_num", Integer, primary_key=True)
    text = Column("text", Unicode)


class Word(Base):
    __tablename__ = "words"
    level_num = Column(
        "level_num",
        Integer,
        ForeignKey("levels.level_num"),
        primary_key=True,
    )
    serial_num = Column("serial_num", Integer, primary_key=True)
    arabic = Column("arabic", Unicode)
    english = Column("english", Unicode)
    examples = relationship("Verse", secondary="examples")


class Example(Base):
    __tablename__ = "examples"
    word_level_num = Column("word_level_num", Integer, primary_key=True)
    word_serial_num = Column("word_serial_num", Integer, primary_key=True)
    verse_sura_num = Column("verse_sura_num", Integer)
    verse_ayah_num = Column("verse_ayah_num", Integer)

    ForeignKeyConstraint(
        [word_level_num, word_serial_num], [Word.level_num, Word.serial_num]
    )
    ForeignKeyConstraint(
        [verse_sura_num, verse_ayah_num], [Verse.sura_num, Verse.ayah_num]
    )


if __name__ == "__main__":
    with Word.get_session() as session:
        print(session.query(Level).count())
        print(session.query(Word).count())
        print(session.query(Verse).count())

        print(session.query(Word.examples))
        words = session.query(Word).filter(Word.level_num == 1).all()
        for word in words:
            print(word.serial_num, word.examples)
