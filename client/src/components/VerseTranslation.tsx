import './VerseTranslation.css';

function VerseTranslation({ translation } : {
  translation: string,
}) {
  return (
    <div className="VerseTranslation">{translation}</div>
  )
}

export default VerseTranslation;
