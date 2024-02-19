from sqlalchemy_wrapper import SQLAlchemy

from .config import CONFIG


db_quran_english = SQLAlchemy(
    uri="sqlite:///app/databases/quran_english.db?check_same_thread=False",
    echo=CONFIG.ECHO_SQL,
)


class QuranEnglish(db_quran_english.Model):  # type: ignore
    __tablename__ = "verses"
    sura_num = db_quran_english.Column(
        "sura", db_quran_english.Integer, primary_key=True
    )
    ayah_num = db_quran_english.Column(
        "ayah", db_quran_english.Integer, primary_key=True
    )
    text = db_quran_english.Column("text", db_quran_english.Unicode)


if __name__ == "__main__":
    print(db_quran_english.session.query(QuranEnglish).count())
