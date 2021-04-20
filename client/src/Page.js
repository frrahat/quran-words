import { useEffect, useState } from "react";
import { useHistory, useLocation, useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";
import WordParts from "./components/WordParts";
import Paginator from "./components/Paginator";

import './Page.css';

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function Page() {
  const { suraNum, ayahNum } = useParams();
  const history = useHistory();
  const query = useQuery();

  const selectedWordIndex = parseInt(query.get('word_index')) || 0;

  const [data, setData] = useState({
    arabic: '',
    english: '',
    words: [],
  });

  const onSelectWordHandler = (index) => {
    history.replace({ search: `word_index=${index}`});
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
      <div className="Page-Paginators">
        <div>
          Sura: {suraNum}
          <Paginator
            currentPage={parseInt(suraNum)}
            max={114}
            getPageLink={(currentPage) => `/verses/${currentPage}/1?word_index=0`} />
        </div>
        <div>
          Ayah: {ayahNum}
          <Paginator
            currentPage={parseInt(ayahNum)}
            max={286}
            getPageLink={(currentPage) => `/verses/${suraNum}/${currentPage}?word_index=0`} />
        </div>
      </div>
      <Verse
        verseArabic={data.arabic}
        corpusWords={data.words}
        onSelectWordHandler={onSelectWordHandler}
        selectedWordIndex={selectedWordIndex} />
      <VerseTranslation translation={data.english} />
      { data.words[selectedWordIndex] &&
        <WordParts wordData={data.words[selectedWordIndex]}/>
      }
    </div>
  );
}

export default Page;
