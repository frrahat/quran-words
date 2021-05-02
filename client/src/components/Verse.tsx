import Word from './Word';

import './Verse.css';


const getWordsData = (verseArabic: string, corpusWords: {
  english: string,
}[]) => {
  const words = verseArabic.split(' ');

  return words.map((word, index) => ({
    arabic: word,
    translation: corpusWords[index]?.english,
  }));
}

function Verse({
  verseArabic,
  corpusWords,
  onSelectWordHandler,
  selectedWordIndex }: {
    verseArabic: string,
    corpusWords: {
      english: string,
    }[],
    onSelectWordHandler: Function,
    selectedWordIndex: number,
  }) {
  return (
    <div className="Verse">
      {getWordsData(verseArabic, corpusWords).map((wordData, index) =>
        <Word
          key={index}
          arabic={wordData.arabic}
          translation={wordData.translation}
          onClickHandler={() => onSelectWordHandler(index)}
          isSelected={selectedWordIndex === index}
        />
      )}
    </div>
  )
}

export default Verse;
