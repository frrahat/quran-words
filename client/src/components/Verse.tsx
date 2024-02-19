import Word from "./Word";

import "./Verse.css";

const getWordsData = (
  verseArabic: string,
  verseWords: {
    english: string;
  }[],
) => {
  const words = verseArabic.split(" ");

  return words.map((word, index) => ({
    arabic: word,
    translation: verseWords[index]?.english,
  }));
};

function Verse({
  verseArabic,
  verseWords,
  onSelectWordHandler,
  selectedWordIndex = -1,
  highlightedWordIndices = [],
}: {
  verseArabic: string;
  verseWords: {
    english: string;
  }[];
  onSelectWordHandler: (selectedWordIndex: number) => void;
  selectedWordIndex?: number;
  highlightedWordIndices?: number[];
}) {
  return (
    <div className="Verse">
      {getWordsData(verseArabic, verseWords).map((wordData, index) => (
        <Word
          key={index}
          arabic={wordData.arabic}
          translation={wordData.translation}
          onClickHandler={() => onSelectWordHandler(index)}
          isSelected={selectedWordIndex === index}
          isHighlighted={highlightedWordIndices.includes(index)}
        />
      ))}
    </div>
  );
}

export default Verse;
