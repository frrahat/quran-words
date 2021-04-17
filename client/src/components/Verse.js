import Word from './Word';

import './Verse.css';


const getWordsData = (verseArabic, corpusWords) => {
  const words = verseArabic.split(' ');

  return words.map((word, index) =>({
    arabic: word,
    translation: corpusWords[index]?.english,
  }));
}

function Verse({ verseArabic, corpusWords }) {
  return (
    <div className="Verse">
      {getWordsData(verseArabic, corpusWords).map((wordData, index) =>
        <Word key={index} arabic={wordData.arabic} translation={wordData.translation} />
      )}
    </div>
  )
}

export default Verse;
