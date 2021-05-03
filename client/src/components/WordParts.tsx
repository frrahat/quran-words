import { MouseEventHandler, useRef } from 'react';
import Segment from './Segment';
import Tooltip from './Tooltip';
import { CorpusWordData, VerbForms } from '../types';

import './WordParts.scss';

const getVerbFormListItem = (verbFormName: string, verbFormValue: string | undefined) =>
  <li><b>{verbFormName}</b>: <span className="WordParts-arabic">{verbFormValue}</span></li>

const getVerbFormsList = (verbForms: VerbForms | undefined) => {
  if (!verbForms) {
    return null;
  }

  const { root, verb_type, perfect, imperative, active_participle, passive_participle, verbal_noun } = verbForms;

  return (
    <ul>
      { getVerbFormListItem('Root', root)}
      { getVerbFormListItem('Verb Type', verb_type)}
      { getVerbFormListItem('Perfect', perfect)}
      { getVerbFormListItem('Imperative', imperative)}
      { getVerbFormListItem('Active Participle', active_participle)}
      { getVerbFormListItem('Passive Participle', passive_participle)}
      { getVerbFormListItem('Verbal Noun', verbal_noun)}
    </ul>
  )
};

function WordParts({ wordData, isWordRootPressed, onWordRootClickHandler }: {
  wordData: CorpusWordData,
  isWordRootPressed: boolean,
  onWordRootClickHandler: MouseEventHandler<HTMLDivElement>,
}) {
  const wordRootRef = useRef(null);

  const { word_num, arabic, english, segments, root, lemma, verb_forms } = wordData;

  return (
    <table className="WordParts">
      <thead>
        <tr>
          <td>#</td>
          <td>Word</td>
          <td>Segments</td>
          <td>Root</td>
          <td>Lemma</td>
          <td>Verb Forms</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{word_num}</td>
          <td>
            <span className="WordParts-word-arabic">{arabic}</span>
            <span className="WordParts-word-english">{english}</span>
          </td>
          <td>
            {
              segments.map((segment, index) => <Segment key={`seg-${index}`} segment={segment} />)
            }
          </td>
          <td>
            {
              root &&
              <Tooltip
                text={`Click to ${isWordRootPressed ? 'hide' : 'show'} occurrences of this word root`}
                childRef={wordRootRef}
              >
                <div
                  className={
                    `WordParts-root WordParts-root${isWordRootPressed ? ' WordParts-root-pressed' : ''
                    }`
                  }
                  onClick={onWordRootClickHandler}
                  ref={wordRootRef}
                >
                  {root}
                </div>
              </Tooltip>
            }
          </td>
          <td><span className="WordParts-arabic">{lemma}</span></td>
          <td>{getVerbFormsList(verb_forms)}</td>
        </tr>
      </tbody>
    </table>
  )
}

export default WordParts;
