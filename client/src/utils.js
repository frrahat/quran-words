const generateQueryString = (wordIndex, shouldShowOccurrences) => {
  let queryString = `word_index=${wordIndex}`;

  if (shouldShowOccurrences) {
    queryString += `&show_occurrences=${shouldShowOccurrences}`;
  }

  return queryString;
};

const generateVersePagePath = (suraNum, ayahNum) =>
  `/app/verses/${suraNum}/${ayahNum}`;

const gerneratePageLink = (suraNum, ayahNum, wordIndex, shouldShowOccurrences) =>
  `${generateVersePagePath(suraNum, ayahNum)}?${generateQueryString(wordIndex, shouldShowOccurrences)}`;

export {
  generateVersePagePath,
  generateQueryString,
  gerneratePageLink,
}
