import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import axios from "axios";

import { gerneratePageLink } from "../utils";
import loaderGif from "../images/loader.gif";

import './Occurrences.css';

function VerseLabel({ suraNum, ayahNum, wordIndex }) {
  return (
    <Link
      className="Occurrences-VerseLabel"
      to={gerneratePageLink(suraNum, ayahNum, wordIndex, true)}
      >
      {suraNum}:{ayahNum}
    </Link>
  )
}

function VerseWord({ word, isHighlighted }) {
  return (
    <span className={`Occurrences-VerseWord${isHighlighted ? '-highlighted': ''}`}>
      {word}
    </span>
  )
}

function Verse({ verse, wordIndex }) {
  return (
    <div className="Occurrences-Verse">
      {verse.split(' ').map((word, index) =>
        <VerseWord
          key={`VerseWord-${index}`}
          word={word}
          isHighlighted={wordIndex === index}
        />
      )}
    </div>
  )
}

function OccurrencesItem({ suraNum, ayahNum, wordIndex, verse}) {
  return (
    <div className="Occurrences-Item">
      <VerseLabel
        suraNum={suraNum}
        ayahNum={ayahNum}
        wordIndex={wordIndex}
      />
      <Verse
        verse={verse}
        wordIndex={wordIndex}
      />
    </div>
  )
}

function Occurrences({ word_root }) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState([]);

  useEffect(() => {
    async function _loadOccurrences() {
      let response;

      try {
        response = await axios.get(`/api/occurrences?root=${word_root}`);
      } catch (err) {
        console.error(err);
      }

      if (response && response.data) {
        setData(response.data.data);
      }

      setIsLoading(false);
    }

    setIsLoading(true);
    _loadOccurrences();
  }, [word_root]);

  return (
    <div className="Occurrences">
      {
        isLoading ?
          <img src={loaderGif} alt="loader" />
          : data.map(({sura, ayah, word_num, verse}, index) => (
          <OccurrencesItem
            key={`Occurrences-${index}`}
            suraNum={sura}
            ayahNum={ayah}
            wordIndex={word_num - 1}
            verse={verse}
          />
        ))
      }
    </div>
  )
}

export default Occurrences;
