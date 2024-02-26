from app.db.db_corpus import POS_FULL_FORMS_AND_COLORS, Corpus


def test_all_pos_forms_are_listed():
    pos_in_db = set()

    with Corpus.get_session() as session:
        for position in range(1, 6):
            pos_in_db = pos_in_db.union(
                {
                    getattr(c, f"pos{position}")
                    for c in session.query(getattr(Corpus, f"pos{position}"))
                    .distinct()
                    .all()
                }
            )

    pos_in_db.remove(None)

    listed_pos = set(POS_FULL_FORMS_AND_COLORS.keys())

    assert pos_in_db.issubset(listed_pos)
