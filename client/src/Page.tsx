import { MouseEventHandler, useEffect, useRef, useState } from "react";
import { useHistory, useLocation, useParams } from "react-router";

import axios from 'axios';

import Verse from "./components/Verse";
import VerseTranslation from "./components/VerseTranslation";
import WordParts from "./components/WordParts";
import Paginator from "./components/Paginator";
import SuraSelect from "./components/SuraSelect";
import AyahSelect from "./components/AyahSelect";
import Occurrences from "./components/Occurrences";
import ExternalLink from "./components/ExternalLink";
import { generateVersePagePath, generatePageSearchString, gerneratePageLink } from "./utils";
import { suraList } from "./config";
import { CorpusWordData } from "./types";

import loaderGif from "./images/loader.gif";
import githubIcon from "./images/github_mark.png";

import './Page.scss';


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

const getResetOccurrencePage = (prevOccurrencePage?: number) =>
  prevOccurrencePage ? 1 : undefined;

function Page() {
  const { suraNum, ayahNum } = useParams<{ suraNum: string, ayahNum: string }>();
  const history = useHistory();
  const query = useQuery();

  const selectedWordIndex = parseInt(query.get('word_index') || '0');
  const occurrencePageQuery = query.get('occurrence_page');
  const occurrencePage = occurrencePageQuery ? parseInt(occurrencePageQuery) : undefined;
  const taraweehDayQuery = query.get('taraweeh_day')
  const taraweehDay = taraweehDayQuery ? parseInt(taraweehDayQuery) : undefined;

  const [data, setData] = useState<CorpusResponseData>(initialData);
  const [isLoading, setIsLoading] = useState(true);

  const pageTopRef = useRef<HTMLDivElement>(null);

  const onGoToTopClickHandler: MouseEventHandler = (event) => {
    pageTopRef.current?.scrollIntoView();

    event.preventDefault();
    event.stopPropagation();
  }

  const updateSelectedWordIndex = (index: number) => {
    if (data.words[index]) {
      history.replace({
        search: generatePageSearchString({
          word_index: index,
          occurrence_page: getResetOccurrencePage(occurrencePage),
          taraweeh_day: taraweehDay,
        }),
      });
    }
  };

  const moveToAyah = (ayahNumToMove: number) => {
    if (ayahNumToMove > 0 && ayahNumToMove <= (suraList[parseInt(suraNum) - 1]?.ayah_count || 0)) {
      history.replace({
        pathname: generateVersePagePath(suraNum, ayahNumToMove),
        search: generatePageSearchString({
          word_index: 0,
          occurrence_page: getResetOccurrencePage(occurrencePage),
          taraweeh_day: taraweehDay,
        }),
      });
    }
  };

  const suraSelectionHandler = (selectedSuraNum: number) => {
    if (selectedSuraNum !== parseInt(suraNum)) {
      history.replace({
        pathname: generateVersePagePath(selectedSuraNum, 1),
        search: generatePageSearchString({
          word_index: 0,
          occurrence_page: getResetOccurrencePage(occurrencePage),
          taraweeh_day: taraweehDay,
        }),
      });
    }
  };

  const ayahSelectionHandler = (selectedAyahNum: number) => {
    if (selectedAyahNum !== parseInt(ayahNum)) {
      history.replace({
        pathname: generateVersePagePath(suraNum, selectedAyahNum),
        search: generatePageSearchString({
          word_index: 0,
          occurrence_page: getResetOccurrencePage(occurrencePage),
          taraweeh_day: taraweehDay,
        }),
      });
    }
  };

  const onWordRootClickHandler: MouseEventHandler<HTMLElement> = (event) => {
    history.replace({
      pathname: generateVersePagePath(suraNum, ayahNum),
      search: generatePageSearchString({
        word_index: selectedWordIndex,
        occurrence_page: occurrencePage ? undefined : 1,
        taraweeh_day: taraweehDay,
      }),
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
    <div className="Page" ref={pageTopRef}>
      <div className="Page-Paginators">
        <div className="Page-Paginator-item">
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
              (currentPage: number) => gerneratePageLink(currentPage, 1, {
                word_index: 0,
                occurrence_page: getResetOccurrencePage(occurrencePage),
                taraweeh_day: taraweehDay,
              })
            } />
        </div>
        <div className="Page-Paginator-item">
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
              (currentPage: number) => gerneratePageLink(suraNum, currentPage, {
                word_index: 0,
                occurrence_page: getResetOccurrencePage(occurrencePage),
                taraweeh_day: taraweehDay,
              })
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
                ].map(({ link, text }) => <ExternalLink link={link} text={text} />)
              }
            </div>
            <VerseTranslation translation={data.english} />
            {data.words[selectedWordIndex] &&
              <WordParts
                wordData={data.words[selectedWordIndex]}
                isWordRootPressed={occurrencePage !== undefined}
                onWordRootClickHandler={onWordRootClickHandler}
              />
            }
            {
              occurrencePage &&
              Boolean(data.words[selectedWordIndex]?.root) &&
              <Occurrences
                wordRoot={data.words[selectedWordIndex]!.root!}
                taraweehDay={taraweehDay}
                occurrencePage={occurrencePage}
                pageTopRef={pageTopRef}
                paginatorLinkGenerator={
                  (currentPage: number) => gerneratePageLink(
                    suraNum, ayahNum, {
                    word_index: selectedWordIndex,
                    occurrence_page: currentPage,
                    taraweeh_day: taraweehDay,
                  })
                }
              />
            }
            <div className="Page-footer">
              <button
                className="Page-goToTop"
                title="Go to top of the page"
                onClick={onGoToTopClickHandler}>
                {String.fromCharCode(8648)}
              </button>
              <a
                className="Page-gitHubLink"
                href="https://github.com/frrahat/quran-words"
                target="_blank"
                rel="noreferrer">
                <img src={githubIcon} alt="github" />
                GitHub
              </a>
            </div>
          </div>
      }
    </div>
  );
}

export default Page;
