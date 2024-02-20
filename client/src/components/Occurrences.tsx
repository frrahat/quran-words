import {
  MouseEventHandler,
  RefObject,
  useEffect,
  useRef,
  useState,
} from "react";
import { useHistory } from "react-router-dom";

import axios from "axios";

import Verse from "./Verse";
import VerseTranslation from "./VerseTranslation";
import Paginator from "./Paginator";
import { gerneratePageLink } from "../utils";
import loaderGif from "../images/loader.gif";
import { formUrlWithQuery } from "../utils";

import "./Occurrences.scss";

type OccurrenceResponseDataItem = {
  sura: number;
  ayah: number;
  word_nums: number[];
  verse: {
    arabic: string;
    english: string;
    words: {
      word_num: number;
      english: string;
    }[];
  };
};

type OccurrenceResponseData = {
  data: OccurrenceResponseDataItem[];
  total: number;
  total_occurrences: number;
};

const initialData = {
  data: [],
  total: 0,
  total_occurrences: 0,
};

function VerseLabel({
  suraNum,
  ayahNum,
  onClickHandler,
}: {
  suraNum: number;
  ayahNum: number;
  onClickHandler: MouseEventHandler;
}) {
  return (
    <button className="Occurrences-VerseLabel" onClick={onClickHandler}>
      {suraNum}:{ayahNum}
    </button>
  );
}

function OccurrencesItem({
  suraNum,
  ayahNum,
  verseArabic,
  verseEnglish,
  verseWords,
  occurredWordIndices,
  navigateToSelectedWord,
}: {
  suraNum: number;
  ayahNum: number;
  verseArabic: string;
  verseEnglish: string;
  verseWords: {
    word_num: number;
    english: string;
  }[];
  occurredWordIndices: number[];
  navigateToSelectedWord: (
    suraNum: number,
    ayahNum: number,
    wordIndex: number,
  ) => void;
}) {
  return (
    <div className="Occurrences-Item">
      <VerseLabel
        suraNum={suraNum}
        ayahNum={ayahNum}
        onClickHandler={(event) => {
          navigateToSelectedWord(suraNum, ayahNum, occurredWordIndices[0]);

          event.preventDefault();
          event.stopPropagation();
        }}
      />
      <div className="Occurrences-Item-verse">
        <Verse
          verseArabic={verseArabic}
          verseWords={verseWords}
          onSelectWordHandler={(wordIndex) =>
            navigateToSelectedWord(suraNum, ayahNum, wordIndex)
          }
          highlightedWordIndices={occurredWordIndices}
        />
      </div>
      <VerseTranslation translation={verseEnglish} />
    </div>
  );
}

function Occurrences({
  wordRoot,
  wordLemma,
  occurrencePage,
  pageTopRef,
  paginatorLinkGenerator,
}: {
  wordRoot: string;
  wordLemma?: string;
  occurrencePage: number;
  pageTopRef: RefObject<HTMLElement>;
  paginatorLinkGenerator: (pageNum: number) => string;
}) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<OccurrenceResponseData>(initialData);

  const occurrencesTopRef = useRef<HTMLDivElement>(null);

  const history = useHistory();

  const navigateToSelectedWord = (
    suraNum: number,
    ayahNum: number,
    wordIndex: number,
  ) => {
    history.push(
      gerneratePageLink(suraNum, ayahNum, {
        word_index: wordIndex,
        occurrence_page: 1,
      }),
    );
    pageTopRef.current?.scrollIntoView();
  };

  const scrollToTop = () => {
    occurrencesTopRef.current?.scrollIntoView();
  };

  const onGoToTopClickHandler: MouseEventHandler<HTMLButtonElement> = (
    event,
  ) => {
    scrollToTop();

    event.preventDefault();
    event.stopPropagation();
  };

  useEffect(() => {
    async function _loadOccurrences() {
      let response:
        | {
            data?: OccurrenceResponseData;
          }
        | undefined;

      const offset = (occurrencePage - 1) * 10;

      try {
        response = await axios.get(
          formUrlWithQuery("/api/occurrences", {
            root: wordRoot,
            lemma: wordLemma,
            offset,
            pageSize: 10,
          }),
          {
            cancelToken: cancelTokenSource.token,
          },
        );
      } catch (err) {
        console.error(err);
      }

      if (response && response.data) {
        setData(response.data);
      }

      setIsLoading(false);
    }

    const cancelTokenSource = axios.CancelToken.source();

    setIsLoading(true);
    _loadOccurrences();

    return () => {
      cancelTokenSource.cancel();
    };
  }, [wordRoot, wordLemma, occurrencePage]);

  const maxPage = Math.ceil(data.total / 10);
  const visibleVerses = Math.min(data.total - (occurrencePage - 1) * 10, 10);

  return (
    <div className="Occurrences">
      <div className="Occurrences-header" ref={occurrencesTopRef}>
        <div className="Occurrences-header-title">
          Occurrences of{" "}
          <span className="Occurrences-header-target">
            {
              `${wordRoot}${wordLemma ? ` >> ${wordLemma}` : ''}`
            }
          </span>
          {isLoading ? (
            ""
          ) : (
            <span className="Occurrences-stat">
              [ {data.total} verse(s), {data.total_occurrences} word(s) ]
            </span>
          )}
        </div>
        {!isLoading && (
          <div className="Occurrences-header-subtitle">
            Showing page {occurrencePage} of {maxPage}{" "}
            <span className="Occurrences-stat">
              [ {visibleVerses} verse(s) ]
            </span>
          </div>
        )}
      </div>
      <div className="Occurrences-body">
        {isLoading ? (
          <div className="Occurrences-loader">
            <img src={loaderGif} alt="loader" />
          </div>
        ) : data.data.length > 0 ? (
          data.data.map(
            (
              { sura, ayah, word_nums, verse: { arabic, english, words } },
              index,
            ) => (
              <OccurrencesItem
                key={`Occurrences-${index}`}
                suraNum={sura}
                ayahNum={ayah}
                verseArabic={arabic}
                verseEnglish={english}
                verseWords={words}
                occurredWordIndices={word_nums.map((word_num) => word_num - 1)}
                navigateToSelectedWord={navigateToSelectedWord}
              />
            ),
          )
        ) : null}
      </div>
      <div className="Occurrences-footer">
        <Paginator
          currentPage={occurrencePage}
          max={maxPage}
          getPageLink={paginatorLinkGenerator}
          onPostPageNavigation={scrollToTop}
        />
        <button
          className="Occurrences-goToTop"
          title="Go to top of the list"
          onClick={onGoToTopClickHandler}
        >
          {String.fromCharCode(8593)}
        </button>
      </div>
    </div>
  );
}

export default Occurrences;
