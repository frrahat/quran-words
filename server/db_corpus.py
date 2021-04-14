from sqlalchemy_wrapper import SQLAlchemy

db_corpus = SQLAlchemy(
    uri='sqlite:///server/databases/corpus.db?check_same_thread=False', echo=True)


class VerbForms(db_corpus.Model):
    __tablename__ = 'verbs_with_six_forms'
    root = db_corpus.Column('root', db_corpus.Unicode, primary_key=True)
    verb_type = db_corpus.Column(
        'verb_type', db_corpus.String(length=3), primary_key=True)
    perfect = db_corpus.Column('perfect', db_corpus.Unicode)
    imperfect = db_corpus.Column('imperfect', db_corpus.Unicode)
    imperative = db_corpus.Column('imperative', db_corpus.Unicode)
    active_participle = db_corpus.Column(
        'active_participle', db_corpus.Unicode)
    passive_participle = db_corpus.Column(
        'passive_participle', db_corpus.Unicode)
    verbal_noun = db_corpus.Column('verbal_noun', db_corpus.Unicode)

    def to_dict(self):
        return {
            'root': self.root,
            'verb_type': self.verb_type,
            'perfect': self.perfect,
            'imperative': self.imperative,
            'active_participle': self.active_participle,
            'passive_participle': self.passive_participle,
            'verbal_noun': self.verbal_noun,
        }


class Corpus(db_corpus.Model):
    __tablename__ = 'corpus'
    sura_num = db_corpus.Column('surah', db_corpus.Integer, primary_key=True)
    ayah_num = db_corpus.Column('ayah', db_corpus.Integer, primary_key=True)
    word_num = db_corpus.Column('word', db_corpus.Integer, primary_key=True)
    count = db_corpus.Column('count', db_corpus.Integer)
    ar1 = db_corpus.Column('ar1', db_corpus.Unicode)
    ar2 = db_corpus.Column('ar2', db_corpus.Unicode)
    ar3 = db_corpus.Column('ar3', db_corpus.Unicode)
    ar4 = db_corpus.Column('ar4', db_corpus.Unicode)
    ar5 = db_corpus.Column('ar5', db_corpus.Unicode)
    pos1 = db_corpus.Column('pos1', db_corpus.Unicode)
    pos2 = db_corpus.Column('pos2', db_corpus.Unicode)
    pos3 = db_corpus.Column('pos3', db_corpus.Unicode)
    pos4 = db_corpus.Column('pos4', db_corpus.Unicode)
    pos5 = db_corpus.Column('pos5', db_corpus.Unicode)
    root = db_corpus.Column('root_ar', db_corpus.Unicode)
    lemma = db_corpus.Column('lemma', db_corpus.Unicode)
    verb_type = db_corpus.Column('verb_type', db_corpus.String(length=3))
    verb_form = db_corpus.Column('verf_form', db_corpus.Integer)
    verb_forms = db_corpus.relationship(
        'VerbForms', uselist=False, lazy='joined')

    db_corpus.ForeignKeyConstraint([root, verb_type],
                                   [VerbForms.root, VerbForms.verb_type])

    def get_segments(self):
        return [
            {
                'segment': getattr(self, 'ar' + str(position)),
                'pos': getattr(self, 'pos'+str(position)),
            } for position in range(1, self.count + 1)
        ]

        # return {
        #     'sura_num': self.sura_num,
        #     'ayah_num': self.ayah_num,
        #     'word_num': self.word_num,
        #     'root': self.root,
        #     'lemma': self.lemma,
        #     'verb_type': self.verb_type,
        #     'verb_form': self.verb_form,
        #     'segments': segments,
        # }


if __name__ == '__main__':
    print(db_corpus.session.query(Corpus).count())
    print(db_corpus.session.query(VerbForms).count())

    base_query = db_corpus.session.query(Corpus).filter(
        Corpus.sura_num == 1, Corpus.ayah_num == 1, Corpus.word_num == 3).first()

    print(base_query.to_dict())
    print(base_query.verb_forms.to_dict())
