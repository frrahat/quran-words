import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import axios from "axios";

import Verse from './Verse';
import { gerneratePageLink } from "../utils";
import loaderGif from "../images/loader.gif";

import './Occurrences.scss';
import VerseTranslation from "./VerseTranslation";

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
  pagination: {
    prev: string | null,
    next: string | null,
  },
}

function VerseLabel({ suraNum, ayahNum, wordIndexToNavigate }: {
  suraNum: number,
  ayahNum: number,
  wordIndexToNavigate: number,
}) {
  return (
    <Link
      className="Occurrences-VerseLabel"
      to={gerneratePageLink(suraNum, ayahNum, wordIndexToNavigate, true)}
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
      <VerseLabel
        suraNum={suraNum}
        ayahNum={ayahNum}
        wordIndexToNavigate={occurredWordIndices[0]}
      />
      <Verse
        verseArabic={verseArabic}
        verseWords={verseWords}
        onSelectWordHandler={() => { }}
        highlightedWordIndices={occurredWordIndices}
      />
      <VerseTranslation translation={verseEnglish}/>
    </div>
  )
}

function Occurrences({ word_root }: {
  word_root: string,
}) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<OccurrenceResponseDataItem[]>([]);

  useEffect(() => {
    async function _loadOccurrences() {
      let response: {
        data?: OccurrenceResponseData,
      } | undefined;

      try {
        response = await axios.get(`/api/occurrences?root=${word_root}`);
      } catch (err) {
        console.error(err);
      }

      if (response && response.data) {
        setData(response.data.data);
      }

      setIsLoading(false);
    }

    setIsLoading(true);
    _loadOccurrences();
  }, [word_root]);

  return (
    <div className="Occurrences">
      {
        isLoading && <img src={loaderGif} alt="loader" />
      }
      {
        !isLoading && data.length > 0 &&
        data.map(({
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
      }
    </div>
  )
}

export default Occurrences;
