import { useEffect, useState } from "react";
import { useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";
import WordParts from "./components/WordParts";

function Page() {
  let { suraNum, ayahNum } = useParams();
  const [data, setData] = useState({
    arabic: '',
    english: '',
    words: [],
  });

  const [selectedWordIndex, setSelectedWordIndex] = useState();

  const onSelectWordHandler = (index) => {
    setSelectedWordIndex(index);
  }

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`/corpus/sura/${suraNum}/ayah/${ayahNum}`);

      setData(response.data);
    }

    fetchData();
  }, [suraNum, ayahNum]);

  return (
    <div>
      <h3>suraNum: {suraNum}</h3>
      <h3>ayahNum: {ayahNum}</h3>
      <Verse
        verseArabic={data.arabic}
        corpusWords={data.words}
        onSelectWordHandler={onSelectWordHandler}
        selectedWordIndex={selectedWordIndex} />
      <VerseTranslation translation={data.english} />
      { selectedWordIndex &&
        <WordParts wordData={data.words[selectedWordIndex]}/>
      }
    </div>
  );
}

export default Page;
