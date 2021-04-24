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

const initialData = {
  arabic: '',
  english: 'Not Found',
  words: [],
};

const getExternalLink = (link, text) => (
  <a
    key={text}
    href={link}
    target="_blank"
    rel="noreferrer">
    {text}
  </a>
);

function Page() {
  const { suraNum, ayahNum } = useParams();
  const history = useHistory();
  const query = useQuery();

  const selectedWordIndex = parseInt(query.get('word_index')) || 0;

  const [data, setData] = useState(initialData);
  const [isLoading, setIsLoading] = useState(true);

  const updateSelectedWordIndex = (index) => {
    if (data.words[index]) {
      history.replace({ search: `word_index=${index}`});
    }
  };

  const moveToAyah = (ayahNumToMove) => {
    if (ayahNumToMove > 0) {
      history.replace({
        pathname: `/verses/${suraNum}/${ayahNumToMove}`,
        search: `word_index=0`,
      });
    }
  };

  useEffect(() => {
    async function fetchData() {
      let response = {
        data: initialData,
      };

      try {
        response = await axios.get(`/corpus/sura/${suraNum}/ayah/${ayahNum}`);
      } catch (err) {
        console.error(err);
      };

      setData(response.data);
      setIsLoading(false);
    }

    setIsLoading(true);
    fetchData();
  }, [suraNum, ayahNum]);

  useEffect(() => {
    const actionMap = {
      'ArrowRight': () => updateSelectedWordIndex(selectedWordIndex - 1),
      'ArrowLeft': () => updateSelectedWordIndex(selectedWordIndex + 1),
      'ArrowUp': () => moveToAyah(parseInt(ayahNum) - 1),
      'ArrowDown': () => moveToAyah(parseInt(ayahNum) + 1),
    }

    const keyDownEventListener = (event) => actionMap[event.code] ? actionMap[event.code]() : null;
    document.addEventListener('keydown', keyDownEventListener);

    return () => {
      document.removeEventListener('keydown', keyDownEventListener);
    }
  });

  return (
    <div className="Page">
      <div className="Page-Paginators">
        <div>
          Sura: <div className="Page-VerseNum">{suraNum}</div>
          <Paginator
            currentPage={parseInt(suraNum)}
            max={114}
            getPageLink={(currentPage) => `/verses/${currentPage}/1?word_index=0`} />
        </div>
        <div>
          Ayah: <div className="Page-VerseNum">{ayahNum}</div>
          <Paginator
            currentPage={parseInt(ayahNum)}
            max={286}
            getPageLink={(currentPage) => `/verses/${suraNum}/${currentPage}?word_index=0`} />
        </div>
      </div>
      {
        isLoading ?
        <div className="Page-Loader">
          <img src="/static/images/loader.gif" alt="loader" />
        </div>
        : <div>
          <Verse
            verseArabic={data.arabic}
            corpusWords={data.words}
            onSelectWordHandler={updateSelectedWordIndex}
            selectedWordIndex={selectedWordIndex} />
          <div className="Page-VerseExternalLinks">
            {
              [
                {
                  link: `https://quran.com/${suraNum}/${ayahNum}`,
                  text: "quran.com",
                },
                {
                  link: `https://corpus.quran.com/wordbyword.jsp?chapter=${suraNum}&verse=${ayahNum}`,
                  text: "corpus.quran.com wordbyword",
                },
                {
                  link: `https://corpus.quran.com/treebank.jsp?chapter=${suraNum}&verse=${ayahNum}`,
                  text: "corpus.quran.com treebank",
                }
              ].map(({ link, text}) => getExternalLink(link, text))
            }
          </div>
          <VerseTranslation translation={data.english} />
          { data.words[selectedWordIndex] &&
            <WordParts wordData={data.words[selectedWordIndex]}/>
          }
        </div>
      }
    </div>
  );
}

export default Page;
