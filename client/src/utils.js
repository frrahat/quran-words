const getVersePageLink = (suraNum, ayahNum, wordIndex=null) =>
 `verses/${suraNum}/${ayahNum}${wordIndex ? `?word_index=${wordIndex}`: ''}`;

export {
  getVersePageLink,
}
