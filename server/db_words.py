from sqlalchemy_wrapper import SQLAlchemy

db_words = SQLAlchemy(
    uri='sqlite:///server/databases/words.db?check_same_thread=False', echo=True)


class Word(db_words.Model):
    __tablename__ = 'allwords'
    sura_num = db_words.Column('sura', db_words.Integer, primary_key=True)
    ayah_num = db_words.Column('ayah', db_words.Integer, primary_key=True)
    word_num = db_words.Column('word', db_words.Integer, primary_key=True)
    english = db_words.Column('en', db_words.Unicode)


if __name__ == '__main__':
    print(db_words.session.query(Word).count())
