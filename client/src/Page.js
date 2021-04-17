import { useEffect, useState } from "react";
import { useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";

function Page() {
  let { suraNum, ayahNum } = useParams();
  const [data, setData] = useState({
    arabic: '',
    english: '',
    words: [],
  });

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
      <Verse verseArabic={data.arabic} corpusWords={data.words} />
      <VerseTranslation translation={data.english} />
    </div>
  );
}

export default Page;
