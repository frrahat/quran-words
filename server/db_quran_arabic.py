from sqlalchemy_wrapper import SQLAlchemy

db_quran_arabic = SQLAlchemy(
    uri='sqlite:///server/databases/quran_arabic.db', echo=True)


class Quran(db_quran_arabic.Model):
    __tablename__ = 'verses'
    sura_num = db_quran_arabic.Column(
        'sura', db_quran_arabic.Integer, primary_key=True)
    ayah_num = db_quran_arabic.Column(
        'ayah', db_quran_arabic.Integer, primary_key=True)
    text = db_quran_arabic.Column('text', db_quran_arabic.Unicode)


if __name__ == '__main__':
    print(db_quran_arabic.session.query(Quran).count())
