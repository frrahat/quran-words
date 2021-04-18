from sqlalchemy_wrapper import SQLAlchemy


db_words_80_percent = SQLAlchemy(
    uri='sqlite:///server/databases/words80percent.db?check_same_thread=False', echo=True)


class Level(db_words_80_percent.Model):  # type: ignore
    num = db_words_80_percent.Column(
        'level_num', db_words_80_percent.Integer, primary_key=True)
    title = db_words_80_percent.Column(
        'level_title', db_words_80_percent.Unicode)


class Verse(db_words_80_percent.Model):  # type: ignore
    sura_num = db_words_80_percent.Column(
        'sura_num', db_words_80_percent.Integer, primary_key=True)
    ayah_num = db_words_80_percent.Column(
        'ayah_num', db_words_80_percent.Integer, primary_key=True)
    text = db_words_80_percent.Column('text', db_words_80_percent.Unicode)


class Word(db_words_80_percent.Model):  # type: ignore
    level_num = db_words_80_percent.Column('level_num', db_words_80_percent.Integer,
                                           db_words_80_percent.ForeignKey(
                                               'levels.level_num'),
                                           primary_key=True)
    serial_num = db_words_80_percent.Column(
        'serial_num', db_words_80_percent.Integer, primary_key=True)
    arabic = db_words_80_percent.Column('arabic', db_words_80_percent.Unicode)
    english = db_words_80_percent.Column(
        'english', db_words_80_percent.Unicode)
    examples = db_words_80_percent.relationship('Verse', secondary='examples')


class Example(db_words_80_percent.Model):  # type: ignore
    word_level_num = db_words_80_percent.Column(
        'word_level_num', db_words_80_percent.Integer, primary_key=True)
    word_serial_num = db_words_80_percent.Column(
        'word_serial_num', db_words_80_percent.Integer, primary_key=True)
    verse_sura_num = db_words_80_percent.Column(
        'verse_sura_num', db_words_80_percent.Integer)
    verse_ayah_num = db_words_80_percent.Column(
        'verse_ayah_num', db_words_80_percent.Integer)

    db_words_80_percent.ForeignKeyConstraint([word_level_num, word_serial_num],
                                             [Word.level_num, Word.serial_num])
    db_words_80_percent.ForeignKeyConstraint([verse_sura_num, verse_ayah_num],
                                             [Verse.sura_num, Verse.ayah_num])


if __name__ == '__main__':
    print(db_words_80_percent.session.query(Level).count())
    print(db_words_80_percent.session.query(Word).count())
    print(db_words_80_percent.session.query(Verse).count())

    print(db_words_80_percent.session.query(Word.examples))
    words = db_words_80_percent.session.query(
        Word).filter(Word.level_num == 1).all()
    for word in words:
        print(word.serial_num, word.examples)
