import Segment from './Segment';

import './WordParts.css';

const getVerbFormListItem = (verbFormName, verbFormValue) =>
  <li><b>{verbFormName}</b>: <span className="WordParts-VerbForm-arabic">{verbFormValue}</span></li>

const getVerbFormsList = (verbForms) => {
  if (!verbForms) {
    return null;
  }

  const { root, verb_type, perfect, imperative, active_participle, passive_participle, verbal_noun } = verbForms;

  return (
    <ul>
      { getVerbFormListItem('Root', root) }
      { getVerbFormListItem('Verb Type', verb_type) }
      { getVerbFormListItem('Perfect', perfect) }
      { getVerbFormListItem('Imperative', imperative) }
      { getVerbFormListItem('Active Participle', active_participle) }
      { getVerbFormListItem('Passive Participle', passive_participle) }
      { getVerbFormListItem('Verbal Noun', verbal_noun) }
    </ul>
  )
};

function WordParts({ wordData }) {
  const { word_num, segments, verb_type, verb_form, verb_forms } = wordData;

  return (
    <table className="WordParts">
      <thead>
        <tr>
          <td>Word Num</td>
          <td>Segments</td>
          <td>Verb Type</td>
          <td>Verb Form</td>
          <td>Verb Forms</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{word_num}</td>
          <td>
          {
            segments.map((segment, index) => <Segment key={`seg-${index}`} segment={segment} />)
          }
          </td>
          <td>{verb_type}</td>
          <td>{verb_form}</td>
          <td>{ getVerbFormsList(verb_forms) }</td>
        </tr>
      </tbody>
    </table>
  )
}

export default WordParts;
