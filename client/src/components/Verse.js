import { useEffect, useRef, useState } from 'react';

import axios from 'axios';

import Tooltip from './Tooltip';

import './Verse.css';


const getWordsData = (verseArabic, corpusWords) => {
  const words = verseArabic.split(' ');

  return words.map((word, index) =>({
    arabic: word,
    translation: corpusWords[index]?.english,
  }));
}

function Verse({ suraNum, ayahNum }) {
  const [data, setData] = useState({
    arabic: '',
    english: '',
    words: [],
  });

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`/corpus/sura/${suraNum}/ayah/${ayahNum}`);

      setData(response.data);
    };

    fetchData();
  }, [suraNum, ayahNum]);

  return (
    <div>
      <div className="Verse-words">{getWordsData(data.arabic, data.words).map((wordData, index) => <Word key={index} arabic={wordData.arabic} translation={wordData.translation} />)}</div>
      <div className="Verse-translation">{data.english}</div>
    </div>
  )
}

function Word({word_id, arabic, translation}) {
  const wordRef = useRef(null);

  return (
    <Tooltip text={translation} childRef={wordRef}>
      <div className="Word" ref={wordRef}>
        <div className="Word-arabic" id={`word-ar-${word_id}`}>
          {arabic}
        </div>
      </div>
    </Tooltip>
  )
}

export default Verse;
