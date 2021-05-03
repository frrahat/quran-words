import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import axios from "axios";

import Verse from './Verse';
import VerseTranslation from "./VerseTranslation";
import Paginator from "./Paginator";
import { gerneratePageLink } from "../utils";
import loaderGif from "../images/loader.gif";

import './Occurrences.scss';


type OccurrenceResponseDataItem = {
  sura: number,
  ayah: number,
  word_nums: number[],
  verse: {
    arabic: string,
    english: string,
    words: {
      word_num: number,
      english: string,
    }[],
  }
}

type OccurrenceResponseData = {
  data: OccurrenceResponseDataItem[],
  total: number,
}

const initialData = {
  data: [],
  total: 0,
}

function VerseLabel({ suraNum, ayahNum, wordIndexToNavigate }: {
  suraNum: number,
  ayahNum: number,
  wordIndexToNavigate: number,
}) {
  return (
    <Link
      className="Occurrences-VerseLabel"
      to={gerneratePageLink(suraNum, ayahNum, wordIndexToNavigate, 1)}
    >
      {suraNum}:{ayahNum}
    </Link>
  )
}

function OccurrencesItem({
  suraNum,
  ayahNum,
  verseArabic,
  verseEnglish,
  verseWords,
  occurredWordIndices,
}: {
  suraNum: number,
  ayahNum: number,
  verseArabic: string,
  verseEnglish: string,
  verseWords: {
    word_num: number,
    english: string,
  }[],
  occurredWordIndices: number[],
}) {
  return (
    <div className="Occurrences-Item">
      <div className="Occurrences-Item-verse">
        <Verse
          verseArabic={verseArabic}
          verseWords={verseWords}
          onSelectWordHandler={() => { /* TODO */ }}
          highlightedWordIndices={occurredWordIndices}
        />
        <VerseLabel
          suraNum={suraNum}
          ayahNum={ayahNum}
          wordIndexToNavigate={occurredWordIndices[0]}
        />
      </div>
      <VerseTranslation translation={verseEnglish} />
    </div>
  )
}

function Occurrences({ wordRoot, occurrencePage, paginatorLinkGenerator }: {
  wordRoot: string,
  occurrencePage: number,
  paginatorLinkGenerator: (pageNum: number) => string,
}) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<OccurrenceResponseData>(initialData);

  useEffect(() => {
    async function _loadOccurrences() {
      let response: {
        data?: OccurrenceResponseData,
      } | undefined;

      const offset = (occurrencePage - 1) * 10;

      try {
        response = await axios.get(
          `/api/occurrences?root=${wordRoot}&offset=${offset}&pagesize=10`, {
          cancelToken: cancelTokenSource.token,
        }
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
    }
  }, [wordRoot, occurrencePage]);

  const maxPage = Math.ceil(data.total / 10);

  return (
    <div className="Occurrences">
      <div className="Occurrences-header">
        <div className="Occurrences-header-title">
          Occurrences of <span className="Occurrences-header-root">{wordRoot}</span> {
            isLoading ? '' : `(${data.total} words)`
          }
        </div>
        {
          !isLoading &&
          <div className="Occurrences-header-subtitle">
            Showing page {occurrencePage} of {maxPage}
          </div>
        }
      </div>
      <div className="Occurrences-body">
        {
          isLoading ?
            <div className="Occurrences-loader">
              <img src={loaderGif} alt="loader" />
            </div>
            : (
              data.data.length > 0 ?
                data.data.map(({
                  sura,
                  ayah,
                  word_nums,
                  verse: { arabic, english, words }
                }, index) => (
                  <OccurrencesItem
                    key={`Occurrences-${index}`}
                    suraNum={sura}
                    ayahNum={ayah}
                    verseArabic={arabic}
                    verseEnglish={english}
                    verseWords={words}
                    occurredWordIndices={word_nums.map(word_num => word_num - 1)}
                  />
                ))
                : null
            )
        }
      </div>
      <div className="Occurrences-footer">
        <Paginator
          currentPage={occurrencePage}
          max={maxPage}
          getPageLink={paginatorLinkGenerator} />
      </div>
    </div>
  )
}

export default Occurrences;
