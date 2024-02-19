export type VerbForms = {
  root: string;
  verb_type: string;
  perfect?: string;
  imperative?: string;
  active_participle?: string;
  passive_participle?: string;
  verbal_noun?: string;
};

export type SegmentData = {
  arabic?: string;
  pos: string;
  pos_full: string;
  pos_color: string;
};

export type CorpusWordData = {
  word_num: number;
  arabic: string;
  english: string;
  segments: SegmentData[];
  root?: string;
  verb_type?: string;
  lemma?: string;
  verb_forms?: VerbForms;
};
