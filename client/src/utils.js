const getVersePageLink = (suraNum, ayahNum, wordIndex = null) =>
  `/app/verses/${suraNum}/${ayahNum}${wordIndex !== null ? `?word_index=${wordIndex}` : ''}`;

export {
  getVersePageLink,
}
