from sqlalchemy_wrapper import SQLAlchemy

db_quran_arabic = SQLAlchemy(
    uri='sqlite:///server/databases/quran_arabic.db?check_same_thread=False', echo=True)


class QuranArabic(db_quran_arabic.Model):  # type: ignore
    __tablename__ = 'verses'
    sura_num = db_quran_arabic.Column(
        'sura', db_quran_arabic.Integer, primary_key=True)
    ayah_num = db_quran_arabic.Column(
        'ayah', db_quran_arabic.Integer, primary_key=True)
    text = db_quran_arabic.Column('text', db_quran_arabic.Unicode)


if __name__ == '__main__':
    print(db_quran_arabic.session.query(QuranArabic).count())
