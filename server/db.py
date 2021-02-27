from sqlalchemy_wrapper import SQLAlchemy


db = SQLAlchemy(uri='sqlite:///server/databases/words.db', echo=True)


class Level(db.Model):
    num = db.Column('level_num', db.Integer, primary_key=True)
    title = db.Column('level_title', db.Unicode)


class Verse(db.Model):
    sura_num = db.Column('sura_num', db.Integer, primary_key=True)
    ayah_num = db.Column('ayah_num', db.Integer, primary_key=True)
    text = db.Column('text', db.Unicode)


class Word(db.Model):
    level_num = db.Column('level_num', db.Integer,
                          db.ForeignKey('levels.level_num'),
                          primary_key=True)
    serial_num = db.Column('serial_num', db.Integer, primary_key=True)
    arabic = db.Column('arabic', db.Unicode)
    english = db.Column('english', db.Unicode)
    examples = db.relationship('Verse', secondary='examples')

class Example(db.Model):
    word_level_num = db.Column('word_level_num', db.Integer, primary_key=True)
    word_serial_num = db.Column('word_serial_num', db.Integer, primary_key=True)
    verse_sura_num = db.Column('verse_sura_num', db.Integer)
    verse_ayah_num = db.Column('verse_ayah_num', db.Integer)

    db.ForeignKeyConstraint([word_level_num, word_serial_num],
                        [Word.level_num, Word.serial_num])
    db.ForeignKeyConstraint([verse_sura_num, verse_ayah_num],
                        [Verse.sura_num, Verse.ayah_num])


if __name__ == '__main__':
    print(db.session.query(Level).count())
    print(db.session.query(Word).count())
    print(db.session.query(Verse).count())

    print(db.session.query(Word.examples))
    words = db.session.query(Word).filter(Word.level_num==1).all()
    for word in words:
        print(word.serial_num, word.examples)
