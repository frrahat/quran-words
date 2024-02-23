import { useRef } from "react";
import Frequencies from "./components/Frequencies";
import Occurrences from "./components/Occurrences";
import { generateWordsPageLink, parseIntFromQuery, useQuery } from "./utils";
import { useHistory } from "react-router";

import "./WordsPage.scss";
import NumberSelect from "./components/NumberSelect";
import Filter from "./components/Filter";

function WordsPage() {
  const history = useHistory();
  const query = useQuery();

  const occurrencePage = parseIntFromQuery(query, "occurrence_page");
  const taraweehNight = parseIntFromQuery(query, "taraweeh_night");
  const frequencyPage = parseIntFromQuery(query, "frequency_page", 0) as number;
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
    <div className="WordsPage" ref={pageTopRef}>
      <div className="WordsPage-FilterPanel">
        <div className="WordsPage-FilterPanelItem">
          <Filter
            filterLabel="Taraweeh night"
            filterValue={taraweehNight}
            selectorComponent={
              <NumberSelect
                valueClassName="WordsPage-FilterPanelItem-numSelect"
                startNumber={1}
                endNumber={27}
                selectedNumber={taraweehNight}
                onSelectNumber={(num) => {
                  const pageLink = generateWordsPageLink({
                    occurrence_page: occurrencePage,
                    taraweeh_night: num,
                    frequency_page: frequencyPage,
                    root: wordRoot,
                    lemma: wordLemma,
                  });

                  history.push(pageLink);
                }}
              />
            }
            onClearAction={() => {
              const pageLink = generateWordsPageLink({
                occurrence_page: occurrencePage,
                taraweeh_night: undefined,
                frequency_page: frequencyPage,
                root: wordRoot,
                lemma: wordLemma,
              });

              history.push(pageLink);
            }}
          />
        </div>
      </div>
      <div className="WordsPage-Content">
        {Boolean(frequencyPage) ? (
          <div className="WordsPage-LeftPanel">
            <Frequencies
              taraweehNight={taraweehNight}
              frequencyPage={frequencyPage}
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
        ) : null}
        {Boolean(wordRoot || wordLemma) ? (
          <div className="WordsPage-RightPanel">
            <Occurrences
              wordRoot={wordRoot}
              wordLemma={wordLemma}
              occurrencePage={occurrencePage || 1}
              pageTopRef={pageTopRef}
              paginatorLinkGenerator={paginatorLinkGenerator}
              taraweehNight={taraweehNight}
            />
          </div>
        ) : (
          <div className="WordsPage-LeftPanel-emptyState">
            Select an item from the frequency list to see occurrences
          </div>
        )}
      </div>
    </div>
  );
}

export default WordsPage;
