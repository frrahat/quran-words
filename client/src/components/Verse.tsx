import Word from './Word';

import './Verse.css';


const getWordsData = (verseArabic: string, verseWords: {
  english: string,
}[]) => {
  const words = verseArabic.split(' ');

  return words.map((word, index) => ({
    arabic: word,
    translation: verseWords[index]?.english,
  }));
}

function Verse({
  verseArabic,
  verseWords,
  onSelectWordHandler,
  selectedWordIndex }: {
    verseArabic: string,
    verseWords: {
      english: string,
    }[],
    onSelectWordHandler: Function,
    selectedWordIndex: number,
  }) {
  return (
    <div className="Verse">
      {getWordsData(verseArabic, verseWords).map((wordData, index) =>
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
