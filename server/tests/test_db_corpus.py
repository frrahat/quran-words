from server.db_corpus import db_corpus, Corpus, POS_FULL_FORMS_AND_COLORS


def test_all_pos_forms_are_listed():
    pos_in_db = set()
    for position in range(1, 6):
        pos_in_db = pos_in_db.union({
            getattr(c, f'pos{position}')
            for c in db_corpus.session.query(
                getattr(Corpus, f'pos{position}')
            )
            .distinct()
            .all()
        })

    pos_in_db.remove(None)

    listed_pos = set(POS_FULL_FORMS_AND_COLORS.keys())

    assert pos_in_db.issubset(listed_pos)
