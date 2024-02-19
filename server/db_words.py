from sqlalchemy_wrapper import SQLAlchemy

from .config import CONFIG


db_words = SQLAlchemy(
    uri='sqlite:///server/databases/words.db?check_same_thread=False',
    echo=CONFIG.ECHO_SQL)


class Word(db_words.Model):  # type: ignore
    __tablename__ = 'allwords'
    sura_num = db_words.Column('sura', db_words.Integer, primary_key=True)
    ayah_num = db_words.Column('ayah', db_words.Integer, primary_key=True)
    word_num = db_words.Column('word', db_words.Integer, primary_key=True)
    english = db_words.Column('en', db_words.Unicode)


if __name__ == '__main__':
    print(db_words.session.query(Word).count())