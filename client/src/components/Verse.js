import { useEffect, useState } from 'react';

import axios from 'axios';

import './Verse.css';

function Verse({ suraNum, ayahNum }) {
  const [arabicText, setArabicText] = useState('');
  const [englishtText, setEnglishText] = useState('');

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`/verses/sura/${suraNum}/ayah/${ayahNum}`);

      const { arabic, english } = response.data;
      setArabicText(arabic);
      setEnglishText(english);
    };

    fetchData();
  }, [suraNum, ayahNum])

  return (
    <div>
      <p className="Verse-arabic">{arabicText.split(' ').map((word, index) => <Word word_id={index} text={word} />)}</p>
      <p className="Verse-english">{englishtText}</p>
    </div>
  )
}

function Word({word_id, text}) {
  return (
    <span className="Word-arabic" id={`word-${word_id}`}>
      {text}
    </span>
  )
}

export default Verse;
