from sqlalchemy_wrapper import SQLAlchemy

db_quran_english = SQLAlchemy(
    uri='sqlite:///server/databases/quran_english.db', echo=True)


class Quran(db_quran_english.Model):
    __tablename__ = 'verses'
    sura_num = db_quran_english.Column(
        'sura', db_quran_english.Integer, primary_key=True)
    ayah_num = db_quran_english.Column(
        'ayah', db_quran_english.Integer, primary_key=True)
    text = db_quran_english.Column('text', db_quran_english.Unicode)


if __name__ == '__main__':
    print(db_quran_english.session.query(Quran).count())
