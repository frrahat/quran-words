import { useRef } from "react";
import Frequencies from "./components/Frequencies";
import Occurrences from "./components/Occurrences";
import { generateWordsPageLink, parseIntFromQuery, useQuery } from "./utils";
import { useHistory } from "react-router";

function WordsPage() {
  const history = useHistory();
  const query = useQuery();

  const occurrencePage = parseIntFromQuery(query, "occurrence_page");
  const taraweehNight = parseIntFromQuery(query, "taraweeh_night");
  const frequencyPage = parseIntFromQuery(query, "frequency_page", 1) as number;
  const wordRoot = query.get("root");
  const wordLemma = query.get("lemma");

  const pageTopRef = useRef<HTMLDivElement>(null);

  const paginatorLinkGenerator = (pageNum: number) =>
    generateWordsPageLink({
      occurrence_page: occurrencePage,
      taraweeh_night: taraweehNight,
      frequency_page: pageNum,
      root: wordRoot,
      lemma: wordLemma,
    });

  return (
    <div className="WordsPage">
      {(wordRoot || wordLemma) && (
        <div className="WordsPage-LeftPanel" ref={pageTopRef}>
          <Occurrences
            wordRoot={wordRoot}
            wordLemma={wordLemma}
            occurrencePage={occurrencePage || 1}
            pageTopRef={pageTopRef}
            paginatorLinkGenerator={paginatorLinkGenerator}
            taraweehNight={taraweehNight}
          />
        </div>
      )}
      <div className="WordsPage-RightPanel">
        <Frequencies
          taraweehNight={taraweehNight}
          frequencyPage={frequencyPage || 1}
          onSelectFrequencyItem={(
            root: string | undefined,
            lemma: string | undefined,
          ) => {
            const pageLink = generateWordsPageLink({
              occurrence_page: occurrencePage,
              taraweeh_night: taraweehNight,
              frequency_page: frequencyPage,
              root: root,
              lemma: lemma,
            });

            history.push(pageLink);
          }}
          paginatorLinkGenerator={paginatorLinkGenerator}
        />
      </div>
    </div>
  );
}

export default WordsPage;
