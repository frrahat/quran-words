import { useEffect, useState } from "react";
import { useHistory, useLocation, useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";
import WordParts from "./components/WordParts";
import Paginator from "./components/Paginator";
import SuraSelect from "./components/SuraSelect";
import AyahSelect from "./components/AyahSelect";
import Occurrences from "./components/Occurrences";
import loaderGif from "./images/loader.gif";
import { generateVersePagePath, generateQueryString, gerneratePageLink } from "./utils";
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
  const shouldShowOccurrences = query.get('show_occurrences') === 'true';

  const [data, setData] = useState(initialData);
  const [isLoading, setIsLoading] = useState(true);

  const updateSelectedWordIndex = (index) => {
    if (data.words[index]) {
      history.replace({
        search: generateQueryString(index, shouldShowOccurrences),
      });
    }
  };

  const moveToAyah = (ayahNumToMove) => {
    if (ayahNumToMove > 0 && ayahNumToMove <= (suraList[suraNum - 1]?.ayah_count || 0)) {
      history.replace({
        pathname: generateVersePagePath(suraNum, ayahNumToMove),
        search: generateQueryString(0, shouldShowOccurrences),
      });
    }
  };

  const suraSelectionHandler = (selectedSuraNum) => {
    if (selectedSuraNum !== parseInt(suraNum)) {
      history.replace({
        pathname: generateVersePagePath(selectedSuraNum, 1),
        search: generateQueryString(0, shouldShowOccurrences),
      });
    }
  };

  const ayahSelectionHandler = (selectedAyahNum) => {
    if (selectedAyahNum !== parseInt(ayahNum)) {
      history.replace({
        pathname: generateVersePagePath(suraNum, selectedAyahNum),
        search: generateQueryString(0, shouldShowOccurrences),
      });
    }
  };

  useEffect(() => {
    async function _loadData() {
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
    _loadData();
  }, [suraNum, ayahNum]);

  useEffect(() => {
    const actionMap = {
      'ArrowRight': () => updateSelectedWordIndex(selectedWordIndex - 1),
      'ArrowLeft': () => updateSelectedWordIndex(selectedWordIndex + 1),
      'ArrowUp': () => moveToAyah(parseInt(ayahNum) - 1),
      'ArrowDown': () => moveToAyah(parseInt(ayahNum) + 1),
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
            getPageLink={
              (currentPage) => gerneratePageLink(currentPage, 1, 0, shouldShowOccurrences)
            } />
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
            getPageLink={
              (currentPage) => gerneratePageLink(suraNum, currentPage, 0, shouldShowOccurrences)
            } />
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
            verseWords={data.words}
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
          {
            shouldShowOccurrences &&
            Boolean(data.words[selectedWordIndex]?.root) &&
            <Occurrences word_root={data.words[selectedWordIndex]?.root} />
          }
        </div>
      }
    </div>
  );
}

export default Page;
