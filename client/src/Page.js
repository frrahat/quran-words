import { useEffect, useState } from "react";
import { useHistory, useLocation, useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";
import WordParts from "./components/WordParts";
import Paginator from "./components/Paginator";
import SuraSelect from "./components/SuraSelect";
import AyahSelect from "./components/AyahSelect";
import loaderGif from "./images/loader.gif";
import { getVersePageLink } from "./utils";
import { suraList } from "./config";

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

  const moveToAyah = (direction) => {
    let nextAyahNum = direction == 'prev' ? ayahNum - 1 : parseInt(ayahNum) + 1;
    let nextSuraNum = suraNum;

    if (nextAyahNum < 1) {
      nextSuraNum = suraNum - 1;
      if (nextSuraNum == 0) {
        nextSuraNum = 114;
      }

      nextAyahNum = suraList[nextSuraNum - 1].ayah_count;
    }

    else if (nextAyahNum > suraList[suraNum -1]?.ayah_count || 0) {
      nextSuraNum = (suraNum % 114) + 1;
      nextAyahNum = 1;
    }

    history.replace({
      pathname: getVersePageLink(nextSuraNum, nextAyahNum),
      search: `word_index=0`,
    });
  };

  const suraSelectionHandler = (selectedSuraNum) => {
    if (selectedSuraNum !== parseInt(suraNum)) {
      history.replace({
        pathname: getVersePageLink(selectedSuraNum, 1),
        search: `word_index=0`,
      });
    }
  };

  const ayahSelectionHandler = (selectedAyahNum) => {
    if (selectedAyahNum !== parseInt(ayahNum)) {
      history.replace({
        pathname: getVersePageLink(suraNum, selectedAyahNum),
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
        response = await axios.get(`/api/corpus/sura/${suraNum}/ayah/${ayahNum}`);
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
      'ArrowUp': () => moveToAyah('prev'),
      'ArrowDown': () => moveToAyah('next'),
    }

    const keyDownEventListener = (event) => {
      if (actionMap[event.code]) {
        actionMap[event.code]();
      }

      event.stopPropagation();
      event.preventDefault();
    };

    document.addEventListener('keydown', keyDownEventListener);

    return () => {
      document.removeEventListener('keydown', keyDownEventListener);
    }
  });

  return (
    <div className="Page">
      <div className="Page-Paginators">
        <div>
          Sura:
          <SuraSelect
            valueClassName="Page-VerseNum"
            selectedSuraNum={suraNum}
            onSelectSura={suraSelectionHandler}
          />
          <Paginator
            currentPage={parseInt(suraNum)}
            max={114}
            getPageLink={(currentPage) => getVersePageLink(currentPage, 1, 0)} />
        </div>
        <div>
          Ayah:
          <AyahSelect
            valueClassName="Page-VerseNum"
            selectedSuraNum={suraNum}
            selectedAyahNum={ayahNum}
            onSelectAyah={ayahSelectionHandler}
          />
          <Paginator
            currentPage={parseInt(ayahNum)}
            max={suraList[suraNum - 1]?.ayah_count || 0}
            getPageLink={(currentPage) => getVersePageLink(suraNum, currentPage, 0)} />
        </div>
      </div>
      {
        isLoading ?
        <div className="Page-Loader">
          <img src={loaderGif} alt="loader" />
        </div>
        : <div>
          <Verse
            verseArabic={data.arabic}
            corpusWords={data.words}
            onSelectWordHandler={updateSelectedWordIndex}
            selectedWordIndex={selectedWordIndex} />
          <div className="Page-VerseExternalLinks">
            {
              data.arabic.length > 0 &&
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
