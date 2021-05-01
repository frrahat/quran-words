import { useEffect, useState } from "react";

import axios from "axios";

import loaderGif from "../images/loader.gif";

import './Occurrences.css';

function Occurrences({ word_root }) {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState([]);

  useEffect(() => {
    async function _loadOccurrences() {
      let response;

      try {
        response = await axios.get(`/api/occurrences?root=${word_root}`);
      } catch (err) {
        console.error(err);
      }

      if (response && response.data) {
        setData(response.data.data);
      }

      setIsLoading(false);
    }

    setIsLoading(true);
    _loadOccurrences();
  }, [word_root]);

  return (
    <div className="Occurrences">
      {
        isLoading ?
          <img src={loaderGif} alt="loader" />
          : data.map(({verse, word_num}, index) => (
          <div key={`Occurrences-${index}`} className="Occurrences-Item">
            {verse}
          </div>
        ))
      }
    </div>
  )
}

export default Occurrences;
