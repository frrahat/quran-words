import { MouseEventHandler, useEffect, useState } from "react";
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

import './Page.scss';
import { CorpusWordData } from "./types";

type CorpusResponseData = {
  sura: number,
  ayah: number,
  arabic: string,
  english: string,
  words: CorpusWordData[],
}

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const initialData = {
  sura: 0,
  ayah: 0,
  arabic: '',
  english: 'Not Found',
  words: [],
};

const getExternalLink = (link: string, text: string): JSX.Element => (
  <a
    key={text}
    href={link}
    target="_blank"
    rel="noreferrer">
    {text}
  </a>
);

const getResetOccurrencePage = (prevOccurrencePage: number) =>
  prevOccurrencePage > 0 ? 1 : 0

function Page() {
  const { suraNum, ayahNum } = useParams<{ suraNum: string, ayahNum: string }>();
  const history = useHistory();
  const query = useQuery();

  const selectedWordIndex = parseInt(query.get('word_index') || '0');
  const occurrencePage = parseInt(query.get('occurrence_page') || '0');

  const [data, setData] = useState<CorpusResponseData>(initialData);
  const [isLoading, setIsLoading] = useState(true);

  const updateSelectedWordIndex = (index: number) => {
    if (data.words[index]) {
      history.replace({
        search: generateQueryString(index, getResetOccurrencePage(occurrencePage)),
      });
    }
  };

  const moveToAyah = (ayahNumToMove: number) => {
    if (ayahNumToMove > 0 && ayahNumToMove <= (suraList[parseInt(suraNum) - 1]?.ayah_count || 0)) {
      history.replace({
        pathname: generateVersePagePath(suraNum, ayahNumToMove),
        search: generateQueryString(0, getResetOccurrencePage(occurrencePage)),
      });
    }
  };

  const suraSelectionHandler = (selectedSuraNum: number) => {
    if (selectedSuraNum !== parseInt(suraNum)) {
      history.replace({
        pathname: generateVersePagePath(selectedSuraNum, 1),
        search: generateQueryString(0, getResetOccurrencePage(occurrencePage)),
      });
    }
  };

  const ayahSelectionHandler = (selectedAyahNum: number) => {
    if (selectedAyahNum !== parseInt(ayahNum)) {
      history.replace({
        pathname: generateVersePagePath(suraNum, selectedAyahNum),
        search: generateQueryString(0, getResetOccurrencePage(occurrencePage)),
      });
    }
  };

  const onWordRootClickHandler: MouseEventHandler<HTMLElement> = (event) => {
    history.replace({
      pathname: generateVersePagePath(suraNum, ayahNum),
      search: generateQueryString(selectedWordIndex, occurrencePage > 0 ? 0 : 1),
    });

    event.preventDefault();
    event.stopPropagation();
  }

  useEffect(() => {
    async function _loadData() {
      let response: { data: CorpusResponseData } = {
        data: initialData,
      };

      try {
        response = await axios.get(`/api/corpus/sura/${suraNum}/ayah/${ayahNum}`, {
          cancelToken: cancelTokenSource.token,
        });
      } catch (err) {
        console.error(err);
      };

      setData(response.data);
      setIsLoading(false);
    }

    const cancelTokenSource = axios.CancelToken.source();

    setIsLoading(true);
    _loadData();

    return () => {
      cancelTokenSource.cancel();
    }

  }, [suraNum, ayahNum]);

  useEffect(() => {
    const actionMap: { [action: string]: Function } = {
      'ArrowRight': () => updateSelectedWordIndex(selectedWordIndex - 1),
      'ArrowLeft': () => updateSelectedWordIndex(selectedWordIndex + 1),
      'ArrowUp': () => moveToAyah(parseInt(ayahNum) - 1),
      'ArrowDown': () => moveToAyah(parseInt(ayahNum) + 1),
    }

    const keyDownEventListener = (event: KeyboardEvent) => {
      if (actionMap[event.code]) {
        actionMap[event.code]();

        event.stopPropagation();
        event.preventDefault();
      }
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
              (currentPage: number) => gerneratePageLink(currentPage, 1, 0, getResetOccurrencePage(occurrencePage))
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
            max={suraList[parseInt(suraNum) - 1]?.ayah_count || 0}
            getPageLink={
              (currentPage: number) => gerneratePageLink(suraNum, currentPage, 0, getResetOccurrencePage(occurrencePage))
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
                ].map(({ link, text }) => getExternalLink(link, text))
              }
            </div>
            <VerseTranslation translation={data.english} />
            {data.words[selectedWordIndex] &&
              <WordParts
                wordData={data.words[selectedWordIndex]}
                isWordRootPressed={occurrencePage > 0}
                onWordRootClickHandler={onWordRootClickHandler}
              />
            }
            {
              occurrencePage > 0 &&
              Boolean(data.words[selectedWordIndex]?.root) &&
              <Occurrences
                wordRoot={data.words[selectedWordIndex]!.root!}
                occurrencePage={occurrencePage}
                paginatorLinkGenerator={
                  (currentPage: number) => gerneratePageLink(
                    suraNum, ayahNum, selectedWordIndex, currentPage
                  )
                }
              />
            }
          </div>
      }
    </div>
  );
}

export default Page;
