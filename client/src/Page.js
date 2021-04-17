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

  const [selectedWordNum, setSelectedWordNum] = useState();

  const onSelectWordHandler = (wordNum) => {
    setSelectedWordNum(wordNum);
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
      <Verse verseArabic={data.arabic} corpusWords={data.words} onSelectWordHandler={onSelectWordHandler}/>
      <VerseTranslation translation={data.english} />
      { selectedWordNum &&
        <WordParts wordData={data.words[selectedWordNum - 1]}/>
      }
    </div>
  );
}

export default Page;
