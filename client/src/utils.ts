const generateQueryString = <QueryObject>(queries: Record<keyof QueryObject, string | number | undefined>) => {
  const queryStrings = Object.entries(queries).map(([key, value]) => value ? `${key}=${value}` : null);
  return queryStrings.filter(str => str).join('&');
};

type PageQueryObject = {
  word_index: number,
  occurrence_page: number | undefined,
  taraweeh_night: number | undefined,
  frequency_item_index: number | undefined,
  frequency_page: number | undefined,
}

const generatePageSearchString = (queryObject: PageQueryObject) =>
  generateQueryString<PageQueryObject>(queryObject);

const generateVersePagePath = (suraNum: string | number, ayahNum: string | number) =>
  `/app/verses/${suraNum}/${ayahNum}`;

const gerneratePageLink = (
  suraNum: string | number,
  ayahNum: string | number,
  queryObject: PageQueryObject) =>
  `${generateVersePagePath(suraNum, ayahNum)}?${generatePageSearchString(queryObject)
  }`;


const formUrlWithQuery = (url: string, queries: object) => {
  return `${url}?${generateQueryString(queries)}`
}

const parseIntFromQuery = (query: string, defaultValue?: number) => {
  return parseInt(query) || defaultValue;
};

export {
  formUrlWithQuery,
  generateVersePagePath,
  gerneratePageLink,
  generatePageSearchString,
  parseIntFromQuery,
}
