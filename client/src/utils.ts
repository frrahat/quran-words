const generateQueryString = (wordIndex: number, occurrencePage: number) => {
  let queryString = `word_index=${wordIndex}`;

  if (occurrencePage > 0) {
    queryString += `&occurrence_page=${occurrencePage}`;
  }

  return queryString;
};

const generateVersePagePath = (suraNum: string | number, ayahNum: string | number) =>
  `/app/verses/${suraNum}/${ayahNum}`;

const gerneratePageLink = (
  suraNum: string | number,
  ayahNum: string | number,
  wordIndex: number,
  occurrencePage: number) =>
  `${generateVersePagePath(suraNum, ayahNum)}?${generateQueryString(wordIndex, occurrencePage)}`;

export {
  generateVersePagePath,
  generateQueryString,
  gerneratePageLink,
}
