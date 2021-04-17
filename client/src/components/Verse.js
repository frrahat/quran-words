import { useEffect, useState } from 'react';

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
      <p className="Verse-words">{getWordsData(data.arabic, data.words).map((wordData, index) => <Word word_id={index} arabic={wordData.arabic} translation={wordData.translation} />)}</p>
      <p className="Verse-translation">{data.english}</p>
    </div>
  )
}

function Word({word_id, arabic, translation}) {
  return (
    <Tooltip text={translation}>
      <div className="Word">
        <div className="Word-arabic" id={`word-ar-${word_id}`}>
          {arabic}
        </div>
      </div>
    </Tooltip>
  )
}

export default Verse;
