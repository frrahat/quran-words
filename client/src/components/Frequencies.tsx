import { MouseEventHandler, useEffect, useState } from "react";
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

const FrequencyItem = ({
  item,
  isSelected,
  onClickItem,
}: {
  item: FrequenceyResponseDataItem;
  isSelected: boolean;
  onClickItem: (item: FrequenceyResponseDataItem) => void;
}) => {
  const onClickHandler: MouseEventHandler<HTMLDivElement> = (event) => {
    event.preventDefault();
    event.stopPropagation();
    onClickItem(item);
  };
  return (
    <div
      className={`FrequencyItem${isSelected ? "--selected" : ""}`}
      onClick={onClickHandler}
    >
      <span className="FrequencyItem-col">{item.lemma}</span>
      <span className="FrequencyItem-col">{item.root}</span>
      <span className="FrequencyItem-col">{item.frequency}</span>
    </div>
  );
};

function Frequencies({
  taraweehNight,
  frequencyPage,
  onSelectFrequencyItem,
  paginatorLinkGenerator,
}: {
  taraweehNight: number | undefined;
  frequencyPage: number;
  onSelectFrequencyItem: (
    root: string | undefined,
    lemma: string | undefined,
  ) => void;
  paginatorLinkGenerator: (pageNum: number) => string;
}) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<FrequenceyResponseData>(initialData);

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
  }, [taraweehNight, frequencyPage]);

  const maxPage = Math.ceil(data.total / PAGE_SIZE);
  const visibleItems = Math.min(
    data.total - (frequencyPage - 1) * PAGE_SIZE,
    PAGE_SIZE,
  );

  const [selectedItemIndex, setSelectedItemIndex] = useState(-1);

  const handleClickOnItem = (
    item: FrequenceyResponseDataItem,
    index: number,
  ) => {
    setSelectedItemIndex(index);
    onSelectFrequencyItem(item.root, item.lemma);
  };

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
          <div>
            {data.data.map((item, index) => (
              <FrequencyItem
                key={index}
                item={item}
                isSelected={index === selectedItemIndex}
                onClickItem={(item) => handleClickOnItem(item, index)}
              />
            ))}
          </div>
        ) : null}
      </div>
      <div className="Frequencies-footer">
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
