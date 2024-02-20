import Frequencies from "./components/Frequencies";
import { generateWordsPageLink, parseIntFromQuery, useQuery } from "./utils";
import { useHistory } from "react-router";

function WordsPage() {
  const history = useHistory();
  const query = useQuery();

  const occurrencePage = parseIntFromQuery(query, "occurrence_page");
  const taraweehNight = parseIntFromQuery(query, "taraweeh_night");
  const frequencyPage = parseIntFromQuery(query, "frequency_page");

  return (
    <Frequencies
      taraweehNight={taraweehNight}
      frequencyPage={frequencyPage || 1}
      frequencyItemIndex={0}
      paginatorLinkGenerator={(currentPage: number) =>
        generateWordsPageLink({
          occurrence_page: occurrencePage,
          taraweeh_night: taraweehNight,
          frequency_item_index: undefined,
          frequency_page: currentPage,
        })
      }
    />
  );
}

export default WordsPage;
