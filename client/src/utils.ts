const generateQueryString = (wordIndex: number, shouldShowOccurrences: boolean) => {
  let queryString = `word_index=${wordIndex}`;

  if (shouldShowOccurrences) {
    queryString += `&show_occurrences=${shouldShowOccurrences}`;
  }

  return queryString;
};

const generateVersePagePath = (suraNum: string | number, ayahNum: string | number) =>
  `/app/verses/${suraNum}/${ayahNum}`;

const gerneratePageLink = (
  suraNum: string | number,
  ayahNum: string | number,
  wordIndex: number,
  shouldShowOccurrences: boolean) =>
  `${generateVersePagePath(suraNum, ayahNum)}?${generateQueryString(wordIndex, shouldShowOccurrences)}`;

export {
  generateVersePagePath,
  generateQueryString,
  gerneratePageLink,
}
