import { useEffect, useState } from "react";
import "./Frequencies.scss";
import { useHistory } from "react-router-dom";
import { formUrlWithQuery, gerneratePageLink } from "../utils";
import loaderGif from "../images/loader.gif";

import axios from "axios";
import Paginator from "./Paginator";

type FrequenceyResponseDataItem = {
  lemma?: string;
  root?: string;
  frequency: number;
};

type FrequenceyResponseData = {
  data: FrequenceyResponseDataItem[];
  total: number;
};

const initialData = {
  data: [],
  total: 0,
};

const PAGE_SIZE = 100;

function Frequencies({
  taraweehNight,
  frequencyPage,
  frequencyItemIndex,
  paginatorLinkGenerator,
}: {
  taraweehNight: number | undefined;
  frequencyPage: number;
  frequencyItemIndex: number;
  paginatorLinkGenerator: (pageNum: number) => string;
}) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<FrequenceyResponseData>(initialData);

  // const history = useHistory();
  // const queryParams = new URLSearchParams(history.location.search);
  // console.log("++++++++", history.location.pathname, queryParams);

  const listOccurencesOnFrequencyItemSelection = () => {
    // history.push(gerneratePageLink(1,1,))
  };

  useEffect(() => {
    async function _loadFrequencies() {
      let response:
        | {
            data?: FrequenceyResponseData;
          }
        | undefined;

      const offset = (frequencyPage - 1) * PAGE_SIZE;

      try {
        response = await axios.get(
          formUrlWithQuery("/api/frequencies", {
            offset: offset,
            pagesize: PAGE_SIZE,
            taraweeh_night: taraweehNight,
          }),
          {
            cancelToken: cancelTokenSource.token,
          },
        );
      } catch (err) {
        console.error(err);
      }

      if (response && response.data) {
        setData(response.data);
      }

      setIsLoading(false);
    }

    const cancelTokenSource = axios.CancelToken.source();

    setIsLoading(true);
    _loadFrequencies();

    return () => {
      cancelTokenSource.cancel();
    };
  }, [taraweehNight, frequencyPage, frequencyItemIndex]);

  const maxPage = Math.ceil(data.total / PAGE_SIZE);
  const visibleItems = Math.min(
    data.total - (frequencyPage - 1) * PAGE_SIZE,
    PAGE_SIZE,
  );

  return (
    <div className="Frequencies">
      <div className="Frequencies-header">
        <div className="Frequencies-header-title">
          {`Frequencies${taraweehNight ? ` in Taraweeh Night: ${taraweehNight}` : ""}`}
        </div>
        {!isLoading && (
          <div className="Frequencies-header-subtitle">
            Showing page {frequencyPage} of {maxPage}{" "}
            <span className="Frequencies-stat">[ {visibleItems} item(s) ]</span>
          </div>
        )}
      </div>
      <div className="Frequencies-body">
        {isLoading ? (
          <div className="Frequencies-loader">
            <img src={loaderGif} alt="loader" />
          </div>
        ) : data.data.length > 0 ? (
          <table>
            <thead>
              <tr>
                <th>Lemma</th>
                <th>Root</th>
                <th>Frequency</th>
              </tr>
            </thead>
            <tbody>
              {data.data.map((item, index) => (
                <tr key={index}>
                  <td>{item.lemma}</td>
                  <td>{item.root}</td>
                  <td>{item.frequency}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
      </div>
      <div className="Occurrences-footer">
        <Paginator
          currentPage={frequencyPage}
          max={maxPage}
          getPageLink={paginatorLinkGenerator}
        />
      </div>
    </div>
  );
}

export default Frequencies;
