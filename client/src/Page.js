import { useEffect, useState } from "react";
import { useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";
import WordParts from "./components/WordParts";
import Paginator from "./components/Paginator";

import './Page.css';

function Page() {
  let { suraNum, ayahNum } = useParams();
  const [data, setData] = useState({
    arabic: '',
    english: '',
    words: [],
  });

  const [selectedWordIndex, setSelectedWordIndex] = useState(0);

  const onSelectWordHandler = (index) => {
    setSelectedWordIndex(index);
  }

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get(`/corpus/sura/${suraNum}/ayah/${ayahNum}`);

      setData(response.data);
    }

    setSelectedWordIndex(0);
    fetchData();
  }, [suraNum, ayahNum]);

  return (
    <div>
      <div className="Page-Paginators">
        <div>
          Sura: {suraNum}
          <Paginator
            currentPage={parseInt(suraNum)}
            max={114}
            getPageLink={(currentPage) => `/verses/${currentPage}/1`} />
        </div>
        <div>
          Ayah: {ayahNum}
          <Paginator
            currentPage={parseInt(ayahNum)}
            max={286}
            getPageLink={(currentPage) => `/verses/${suraNum}/${currentPage}`} />
        </div>
      </div>
      <Verse
        verseArabic={data.arabic}
        corpusWords={data.words}
        onSelectWordHandler={onSelectWordHandler}
        selectedWordIndex={selectedWordIndex} />
      <VerseTranslation translation={data.english} />
      { data.words.length &&
        <WordParts wordData={data.words[selectedWordIndex]}/>
      }
    </div>
  );
}

export default Page;
